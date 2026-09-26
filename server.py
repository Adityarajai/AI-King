import base64
import datetime as dt
import hashlib
import html
import json
import os
import secrets
import sqlite3
import urllib.parse
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT, "analytics.sqlite3")
MAX_QUERY_LENGTH = 2000


def db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS search_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                visitor_id TEXT NOT NULL,
                query TEXT NOT NULL,
                created_at TEXT NOT NULL,
                device TEXT NOT NULL,
                user_agent TEXT NOT NULL,
                consent_version TEXT NOT NULL
            )
            """
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_search_events_created_at "
            "ON search_events(created_at DESC)"
        )


def visitor_id_from_request(handler):
    cookies = SimpleCookie()
    cookies.load(handler.headers.get("Cookie", ""))
    value = cookies.get("ai_king_visitor")
    if value and value.value and len(value.value) <= 100:
        return value.value, False
    return secrets.token_urlsafe(18), True


def device_from_user_agent(user_agent):
    agent = user_agent.lower()
    if "tablet" in agent or "ipad" in agent:
        return "Tablet"
    if any(token in agent for token in ("mobile", "android", "iphone")):
        return "Mobile"
    return "Desktop"


def clean_query(value):
    if not isinstance(value, str):
        return ""
    return " ".join(value.split())[:MAX_QUERY_LENGTH]


def wants_json(handler):
    return "application/json" in handler.headers.get("Accept", "")


def json_response(handler, payload, status=HTTPStatus.OK, extra_headers=None):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    for name, value in (extra_headers or []):
        handler.send_header(name, value)
    handler.end_headers()
    handler.wfile.write(body)


def admin_authorized(handler):
    password = os.environ.get("ADMIN_PASSWORD", "")
    if not password:
        return False
    header = handler.headers.get("Authorization", "")
    if not header.startswith("Basic "):
        return False
    try:
        decoded = base64.b64decode(header[6:]).decode("utf-8")
        _, supplied_password = decoded.split(":", 1)
    except (ValueError, UnicodeDecodeError):
        return False
    return secrets.compare_digest(supplied_password, password)


def require_admin(handler):
    if admin_authorized(handler):
        return True
    handler.send_response(HTTPStatus.UNAUTHORIZED)
    handler.send_header("WWW-Authenticate", 'Basic realm="AI King Analytics"')
    handler.send_header("Content-Type", "text/plain; charset=utf-8")
    handler.end_headers()
    handler.wfile.write(b"Admin authentication required.")
    return False


def admin_page():
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI King • Private Analytics</title>
  <style>
    :root { color-scheme: dark; --cyan:#55e7ff; --violet:#9d7aff; --gold:#f5c451; }
    * { box-sizing:border-box; }
    body { margin:0; min-height:100vh; padding:32px; font-family:Inter,ui-sans-serif,system-ui,sans-serif;
      color:#eef2ff; background:radial-gradient(circle at 10% 0%,#15313e,transparent 35%),#070a11; }
    main { width:min(1100px,100%); margin:auto; }
    .top { display:flex; justify-content:space-between; align-items:end; gap:20px; margin-bottom:28px; }
    h1 { margin:0 0 8px; font-size:clamp(1.8rem,4vw,3rem); letter-spacing:-.04em; }
    .eyebrow { color:var(--cyan); font-size:.7rem; font-weight:700; letter-spacing:.18em; }
    .muted { color:#91a0b7; }
    .cards { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-bottom:24px; }
    .card, .table-wrap { border:1px solid rgba(85,231,255,.16); background:rgba(17,24,36,.78);
      border-radius:18px; box-shadow:0 16px 50px rgba(0,0,0,.2); }
    .card { padding:20px; }
    .label { color:#91a0b7; font-size:.75rem; text-transform:uppercase; letter-spacing:.12em; }
    .value { display:block; margin-top:10px; color:#fff; font-size:2rem; font-weight:750; }
    .table-wrap { overflow:auto; }
    table { width:100%; border-collapse:collapse; min-width:700px; }
    th,td { padding:15px 18px; text-align:left; border-bottom:1px solid rgba(255,255,255,.07); }
    th { color:var(--cyan); font-size:.7rem; text-transform:uppercase; letter-spacing:.12em; }
    td { color:#dfe7f6; font-size:.9rem; }
    .query { max-width:460px; color:#fff; word-break:break-word; }
    .pill { display:inline-block; padding:5px 9px; border-radius:99px; color:#071017;
      background:linear-gradient(135deg,#b8f7ff,#55e7ff); font-size:.7rem; font-weight:700; }
    @media (max-width:650px) { body { padding:20px 14px; } .top { display:block; } .cards { grid-template-columns:1fr; } }
  </style>
</head>
<body>
<main>
  <div class="top">
    <div><div class="eyebrow">PRIVATE ADMIN CONSOLE</div><h1>AI King Analytics</h1>
      <div class="muted">Anonymous, consent-based search activity.</div></div>
    <div class="muted">No passwords or personal identity collected</div>
  </div>
  <section class="cards">
    <div class="card"><span class="label">Total searches</span><strong class="value" id="total">—</strong></div>
    <div class="card"><span class="label">Unique visitors</span><strong class="value" id="visitors">—</strong></div>
    <div class="card"><span class="label">Last 24 hours</span><strong class="value" id="recent">—</strong></div>
  </section>
  <div class="table-wrap"><table><thead><tr><th>Time</th><th>Visitor</th><th>Search</th><th>Device</th></tr></thead>
    <tbody id="rows"><tr><td colspan="4" class="muted">Loading…</td></tr></tbody></table></div>
</main>
<script>
  const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) =>
    ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  fetch('/api/admin/events', { headers: { Accept: 'application/json' } })
    .then((response) => response.ok ? response.json() : Promise.reject(new Error('Unable to load analytics')))
    .then((data) => {
      document.querySelector('#total').textContent = data.summary.total;
      document.querySelector('#visitors').textContent = data.summary.unique_visitors;
      document.querySelector('#recent').textContent = data.summary.last_24_hours;
      document.querySelector('#rows').innerHTML = data.events.length ? data.events.map((event) => `
        <tr><td>${escapeHtml(new Date(event.created_at).toLocaleString())}</td>
        <td><span class="pill">${escapeHtml(event.visitor_id)}</span></td>
        <td class="query">${escapeHtml(event.query)}</td><td>${escapeHtml(event.device)}</td></tr>`).join('')
        : '<tr><td colspan="4" class="muted">No consented searches yet.</td></tr>';
    })
    .catch((error) => { document.querySelector('#rows').innerHTML = `<tr><td colspan="4">${escapeHtml(error.message)}</td></tr>`; });
</script>
</body>
</html>"""


class AIKingHandler(SimpleHTTPRequestHandler):
    server_version = "AIKing/1.0"

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        super().end_headers()

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/admin":
            if require_admin(self):
                body = admin_page().encode("utf-8")
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            return
        if path == "/api/admin/events":
            if not require_admin(self):
                return
            with db_connection() as connection:
                events = connection.execute(
                    "SELECT visitor_id, query, created_at, device FROM search_events "
                    "ORDER BY id DESC LIMIT 500"
                ).fetchall()
                total = connection.execute("SELECT COUNT(*) FROM search_events").fetchone()[0]
                unique_visitors = connection.execute(
                    "SELECT COUNT(DISTINCT visitor_id) FROM search_events"
                ).fetchone()[0]
                recent = connection.execute(
                    "SELECT COUNT(*) FROM search_events "
                    "WHERE datetime(created_at) >= datetime('now', '-1 day')"
                ).fetchone()[0]
            json_response(self, {
                "summary": {
                    "total": total,
                    "unique_visitors": unique_visitors,
                    "last_24_hours": recent,
                },
                "events": [dict(event) for event in events],
            })
            return
        return super().do_GET()

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if path != "/api/analytics":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        try:
            length = min(int(self.headers.get("Content-Length", "0")), 10000)
            payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            json_response(self, {"error": "Invalid event"}, HTTPStatus.BAD_REQUEST)
            return

        query = clean_query(payload.get("query"))
        if payload.get("consent") is not True or not query:
            json_response(self, {"recorded": False})
            return

        visitor_id, is_new = visitor_id_from_request(self)
        user_agent = self.headers.get("User-Agent", "")[:500]
        created_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
        with db_connection() as connection:
            connection.execute(
                "INSERT INTO search_events "
                "(visitor_id, query, created_at, device, user_agent, consent_version) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (visitor_id, query, created_at, device_from_user_agent(user_agent),
                 "", "2026-09-26"),
            )
        headers = []
        if is_new:
            headers.append(("Set-Cookie", f"ai_king_visitor={visitor_id}; Path=/; Max-Age=31536000; SameSite=Lax"))
        json_response(self, {"recorded": True}, extra_headers=headers)


if __name__ == "__main__":
    initialize_database()
    port = int(os.environ.get("PORT", "5000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), AIKingHandler)
    print(f"AI King server listening on port {port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()