# ✨ [feature] store: todo ids become UUIDs
## Problem
Sequential ids leak how many todos exist and collide when two stores are merged.

## Context
- **Where:** `src/lab/store.py`, `src/lab/app.py`
  - a. Create a todo and read its `id`
- **Who:** every API client (the id format changes)

## Fix
Generate todo ids with `uuid4` and accept them in every `/todos/{todo_id}` route.

## Acceptance Criteria
- [ ] A created todo's `id` is a version-4 UUID string
- [ ] `GET`, `PATCH`, `DELETE` and `POST …/toggle` on `/todos/{id}` work with the UUID and return 404 for an unknown UUID
- [ ] A non-UUID id returns 404, not 500

## Risk
🔴 **High** · changes the stored data shape and every client's ids

## Blocked by
- None.
