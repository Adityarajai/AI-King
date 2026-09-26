const crypto = require("node:crypto");
const { getStore } = require("@netlify/blobs");

const MAX_QUERY_LENGTH = 2000;
const STORE_NAME = "ai-king-analytics";

function json(statusCode, payload, headers = {}) {
  return {
    statusCode,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store",
      ...headers,
    },
    body: JSON.stringify(payload),
  };
}

function visitorIdFromCookie(cookieHeader) {
  const match = (cookieHeader || "").match(/(?:^|;\s*)ai_king_visitor=([^;]+)/);
  if (match && /^[A-Za-z0-9_-]{10,100}$/.test(match[1])) {
    return { value: match[1], isNew: false };
  }
  return { value: crypto.randomBytes(18).toString("base64url"), isNew: true };
}

function deviceFromUserAgent(userAgent = "") {
  const agent = userAgent.toLowerCase();
  if (agent.includes("tablet") || agent.includes("ipad")) return "Tablet";
  if (["mobile", "android", "iphone"].some((token) => agent.includes(token))) return "Mobile";
  return "Desktop";
}

function cleanQuery(value) {
  if (typeof value !== "string") return "";
  return value.replace(/\s+/g, " ").trim().slice(0, MAX_QUERY_LENGTH);
}

function adminIsAuthorized(event) {
  const password = process.env.ADMIN_PASSWORD || "";
  const header = event.headers?.authorization || event.headers?.Authorization || "";
  if (!password || !header.startsWith("Basic ")) return false;
  try {
    const decoded = Buffer.from(header.slice(6), "base64").toString("utf8");
    const separator = decoded.indexOf(":");
    const supplied = separator >= 0 ? decoded.slice(separator + 1) : "";
    return supplied.length === password.length &&
      crypto.timingSafeEqual(Buffer.from(supplied), Buffer.from(password));
  } catch {
    return false;
  }
}

function requireAdmin(event) {
  if (adminIsAuthorized(event)) return null;
  return {
    statusCode: 401,
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "WWW-Authenticate": 'Basic realm="AI King Analytics"',
      "Cache-Control": "no-store",
    },
    body: "Admin authentication required.",
  };
}

async function listEvents(store) {
  const events = [];
  for await (const page of store.list({ prefix: "event-", paginate: true })) {
    for (const blob of page.blobs) {
      const event = await store.get(blob.key, { type: "json" });
      if (event) events.push(event);
    }
  }
  return events.sort((a, b) => b.created_at.localeCompare(a.created_at)).slice(0, 500);
}

exports.handler = async (event) => {
  const method = event.httpMethod || "GET";
  const store = getStore(STORE_NAME);

  if (method === "POST") {
    let payload;
    try {
      payload = JSON.parse(event.body || "{}");
    } catch {
      return json(400, { error: "Invalid event" });
    }

    const query = cleanQuery(payload.query);
    if (payload.consent !== true || !query) return json(200, { recorded: false });

    const visitor = visitorIdFromCookie(event.headers?.cookie || event.headers?.Cookie);
    const userAgent = event.headers?.["user-agent"] || event.headers?.["User-Agent"] || "";
    const createdAt = new Date().toISOString();
    const key = `event-${Date.now()}-${crypto.randomBytes(8).toString("hex")}`;

    await store.setJSON(key, {
      visitor_id: visitor.value,
      query,
      created_at: createdAt,
      device: deviceFromUserAgent(userAgent),
      consent_version: "2026-09-26",
    });

    const headers = {};
    if (visitor.isNew) {
      headers["Set-Cookie"] = `ai_king_visitor=${visitor.value}; Path=/; Max-Age=31536000; SameSite=Lax`;
    }
    return json(200, { recorded: true }, headers);
  }

  if (method === "GET") {
    const unauthorized = requireAdmin(event);
    if (unauthorized) return unauthorized;

    const events = await listEvents(store);
    const cutoff = Date.now() - 24 * 60 * 60 * 1000;
    return json(200, {
      summary: {
        total: events.length,
        unique_visitors: new Set(events.map((item) => item.visitor_id)).size,
        last_24_hours: events.filter((item) => Date.parse(item.created_at) >= cutoff).length,
      },
      events,
    });
  }

  return json(405, { error: "Method not allowed" }, { Allow: "GET, POST" });
};