# AI King

## Run

The app runs with:

```bash
python3 server.py
```

The `Start application` workflow serves the site on port 5000.

## Private analytics

Visitors see a consent banner before search events are recorded. If they allow
anonymous analytics, the server stores the search text, an anonymous visitor
ID, timestamp, and broad device category in `analytics.sqlite3`.

The private dashboard is available at `/admin`. It uses HTTP Basic
Authentication with username `admin` and the `ADMIN_PASSWORD` Replit Secret.
No password or personal identity is recorded as an analytics event.

## Netlify deployment

The repository also includes a Netlify-compatible implementation:

- `netlify/functions/analytics.js` stores consented events in Netlify Blobs
- `admin.html` is the static dashboard
- `netlify.toml` routes `/api/analytics`, `/api/admin/events`, and `/admin`

In Netlify Site configuration, add an environment variable named
`ADMIN_PASSWORD` before deploying. Netlify environment variables are separate
from Replit Secrets. The Netlify Blobs store is created and managed by the
Netlify Functions integration.