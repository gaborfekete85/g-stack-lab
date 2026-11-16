# ✨ [feature] todos: limit how many todos the list returns
## Problem
`GET /todos` always returns every todo. Clients that only show the first few still download them all.

## Context
- **Where:** todos API, `GET /todos`
  - a. Create three todos
  - b. Request `GET /todos?limit=2`
- **Who:** API clients and the web UI

## Fix
Accept an optional positive integer `limit` that returns at most that many todos, oldest first. It combines with `status`.

## Acceptance Criteria
- [ ] With three todos, `GET /todos?limit=2` returns exactly the todos with ids 1 and 2
- [ ] `GET /todos?limit=0` and `GET /todos?limit=-1` return 400
- [ ] `GET /todos` without `limit` returns all three todos

## Risk
🟢 **Low** · additive query parameter on one route

## Blocked by
- None.
