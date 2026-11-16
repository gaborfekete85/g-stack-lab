# ✨ [feature] todos: counts of open and done todos in one call
## Problem
To show "3 open · 2 done", a client has to download every todo and count them itself.

## Context
- **Where:** todos API, `GET /todos/stats`
  - a. Create three todos
  - b. Complete one of them
  - c. Send `GET /todos/stats`
- **Who:** API clients and the web UI

## Fix
Add `GET /todos/stats` that returns the number of open, done and all todos.

## Acceptance Criteria
- [ ] With three todos and one completed, `GET /todos/stats` returns 200 with `{"open": 2, "done": 1, "total": 3}`
- [ ] With no todos, it returns `{"open": 0, "done": 0, "total": 0}`
- [ ] A todo completed and then reopened counts as open, not done

## Risk
🟢 **Low** · read-only endpoint

## Blocked by
- None.
