# ✨ [feature] app: health endpoint for uptime checks
## Problem
An uptime monitor has no cheap URL to call: every endpoint touches the todo store.

## Context
- **Where:** `GET /health`
  - a. Start the app
  - b. Send `GET /health`
- **Who:** uptime monitors, deploy scripts

## Fix
Add `GET /health` that returns a fixed body without reading the store.

## Acceptance Criteria
- [ ] `GET /health` returns 200 with `{"status": "ok"}`
- [ ] `GET /health` still returns 200 with `{"status": "ok"}` when the store holds 3 todos

## Risk
🟢 **Low** · new read-only route

## Blocked by
- None.
