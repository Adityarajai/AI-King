---
name: Netlify Blobs in Lambda handlers
description: Netlify Blobs initialization behavior for CommonJS Lambda-compatible functions.
---

Netlify Blobs may not receive its automatic execution context when a function uses the Lambda-compatible handler format. Call `connectLambda(event)` before `getStore(...)`.

**Why:** Without the initialization, deployed requests fail with `MissingBlobsEnvironmentError` even though the package and store name are correct.

**How to apply:** In Netlify Functions that export `handler(event)`, initialize the Blobs context at the start of the handler, before any store access.