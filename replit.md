# AI King

## Run

The app runs with:

```bash
python3 server.py
```

The `Start application` workflow serves the site on port 5000.

## Private analytics

Visitors are asked for their name before search events are recorded. If they
continue, the server stores the name, search text, an anonymous visitor ID,
timestamp, and broad device category in `analytics.sqlite3`. Visitors can skip
the prompt; skipped visitors are not recorded.

The private dashboard is available at `/admin`. It uses HTTP Basic
Authentication with username `admin` and the `ADMIN_PASSWORD` Replit Secret.
The name prompt explains that the name and consented searches appear in the
private dashboard. Passwords are never recorded as analytics events.

## Netlify deployment

The repository also includes a Netlify-compatible implementation:

- `netlify/functions/analytics.js` stores consented events in Netlify Blobs
- `admin.html` is the static dashboard
- `netlify.toml` routes `/api/analytics`, `/api/admin/events`, and `/admin`

In Netlify Site configuration, add an environment variable named
`ADMIN_PASSWORD` before deploying. Netlify environment variables are separate
from Replit Secrets. The Netlify Blobs store is created and managed by the
Netlify Functions integration.