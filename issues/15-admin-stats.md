# ✨ [feature] auth: admin-only stats behind a token
## Problem
Operators want todo counts from a monitoring script, but the endpoint must not be public.

## Context
- **Where:** `GET /admin/stats`
  - a. Set `LAB_ADMIN_TOKEN=s3cret` in the environment
  - b. Send `GET /admin/stats` with header `X-Admin-Token: s3cret`
- **Who:** operators' monitoring scripts

## Fix
Add `GET /admin/stats` returning `{"total": N}`, only when the `X-Admin-Token` header equals the `LAB_ADMIN_TOKEN` environment variable.

## Acceptance Criteria
- [ ] With `LAB_ADMIN_TOKEN=s3cret` and header `X-Admin-Token: s3cret`, `GET /admin/stats` returns 200 with `{"total": 2}` when there are 2 todos
- [ ] A wrong or missing header returns 401 with `{"error": "admin token required"}`
- [ ] When `LAB_ADMIN_TOKEN` is not set, every request returns 401 (no token means no access)

## Risk
🟡 **Medium** · access control; a mistake exposes data

## Blocked by
- None.
