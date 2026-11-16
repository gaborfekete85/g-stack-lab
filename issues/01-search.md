# ✨ [feature] todos: search titles with a q parameter
## Problem
With many todos there is no way to find one by name. Users scroll the whole list.

## Context
- **Where:** todos API, `GET /todos`
  - a. Create todos "Buy milk", "Call mom", "buy bread"
  - b. Request `GET /todos?q=buy`
- **Who:** API clients and the web UI

## Fix
Accept an optional `q` query parameter that keeps only todos whose title contains it, ignoring case. It combines with `status`.

## Acceptance Criteria
- [ ] `GET /todos?q=buy` returns "Buy milk" and "buy bread" and not "Call mom"
- [ ] `GET /todos?q=buy&status=done` returns only completed todos whose title contains "buy"
- [ ] `GET /todos?q=` (empty) returns the same list as no `q`

## Risk
🟢 **Low** · additive query parameter on one route

## Blocked by
- None.
