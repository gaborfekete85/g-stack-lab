# 🐛 [bug] todos: reopened todo vanishes from the open filter
## Problem
A todo that was completed and then unchecked again no longer appears under "open". It looks deleted.

## Context
- **Where:** todos API, `GET /todos?status=open`
  - a. Create a todo
  - b. Toggle it to done
  - c. Toggle it back to open
  - d. Request `GET /todos?status=open`
- **Who:** every user who unchecks a todo

## Evidence
- Saw: `GET /todos?status=open` returns `[]`
- Expected: the reopened todo is in the list
- Reproduced: in-memory store, 2026-11-16

## Fix
Reopening a todo must leave it in the same state as a todo that was never completed.

## Acceptance Criteria
- [ ] After done-then-reopen, `GET /todos?status=open` includes the todo
- [ ] After done-then-reopen, the todo's `completedAt` is `null`
- [ ] `GET /todos?status=done` does not include the reopened todo

## Risk
🟢 **Low** · one store function

## Blocked by
- None.
