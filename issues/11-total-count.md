# ✨ [feature] todos: X-Total-Count header on the todo list
## Problem
A client that shows "showing 2 of 5" has to make a second call to learn the total.

## Context
- **Where:** `GET /todos`
  - a. Create three todos, complete one
  - b. Send `GET /todos?status=open`
- **Who:** API clients and the web UI

## Fix
Add an `X-Total-Count` header with the number of todos in the response.

## Acceptance Criteria
- [ ] With three todos, `GET /todos` has header `X-Total-Count: 3`
- [ ] With three todos and one completed, `GET /todos?status=open` has header `X-Total-Count: 2`
- [ ] With no todos, `GET /todos` has header `X-Total-Count: 0`

## Risk
🟢 **Low** · response header only

## Blocked by
- None.
