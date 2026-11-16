# ✨ [feature] todos: clear all completed todos at once
## Problem
Completed todos pile up. Removing them means one DELETE per todo.

## Context
- **Where:** todos API, `DELETE /todos?status=done`
  - a. Create three todos
  - b. Complete two of them
  - c. Send `DELETE /todos?status=done`
- **Who:** API clients and the web UI

## Fix
Add `DELETE /todos?status=done` that removes every completed todo and returns how many it removed.

## Acceptance Criteria
- [ ] `DELETE /todos?status=done` returns 200 with `{ "removed": 2 }` after two of three todos were completed
- [ ] After the call, `GET /todos` returns only the open todo
- [ ] `DELETE /todos` without `status=done` returns 400 and removes nothing

## Risk
🟡 **Medium** · bulk delete; a wrong filter loses data

## Blocked by
- None.
