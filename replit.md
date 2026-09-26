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