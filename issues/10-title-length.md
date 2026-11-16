# ✨ [feature] todos: reject titles longer than 200 characters
## Problem
A client can create a todo with a title of any length, which breaks the list layout.

## Context
- **Where:** `POST /todos`, `PATCH /todos/{id}`
  - a. Send `POST /todos` with a 201-character title
- **Who:** API clients

## Fix
Reject titles longer than 200 characters on create and rename.

## Acceptance Criteria
- [ ] `POST /todos` with a 201-character title returns 400 with `{"error": "title must be at most 200 characters"}` and creates nothing
- [ ] `POST /todos` with a 200-character title returns 201
- [ ] `PATCH /todos/{id}` with a 201-character title returns 400 with the same error and keeps the old title

## Risk
🟢 **Low** · input validation on two routes

## Blocked by
- None.
