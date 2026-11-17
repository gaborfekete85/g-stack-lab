# ✨ [feature] todos: get the oldest open todo
## Problem
A client that shows "the next thing to do" has to fetch every todo and sort them itself.

## Context
- **Where:** `src/lab/app.py`, new route `GET /todos/oldest`
  - a. Create three todos
  - b. Send `GET /todos/oldest`
- **Who:** API clients

## Fix
Add `GET /todos/oldest` returning the open todo with the earliest `created_at`.

## Acceptance Criteria
- [ ] With three open todos, `GET /todos/oldest` returns 200 with the first one created
- [ ] A completed todo is never returned, even when it is the oldest
- [ ] With no open todos it returns 404 with `{"error": "no open todos"}`

## Risk
🟡 **Medium** · new route next to `/todos/{todo_id}`; route order matters

## Blocked by
- None.
