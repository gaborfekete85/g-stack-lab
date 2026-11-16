# ♻️ [refactor] app: one todo lookup instead of four copies
## Problem
Four route handlers each repeat the same "find todo or return 404" code. A change to the 404 body has to be made four times and is easy to miss.

## Context
- **Where:** `src/app.ts`
  - a. `GET /todos/:id`
  - b. `POST /todos/:id/toggle`
  - c. `PATCH /todos/:id`
  - d. `DELETE /todos/:id`
- **Who:** developers

## Fix
Do the id lookup and the 404 in one place that all four routes use. Behaviour stays the same.

## Acceptance Criteria
- [ ] The 404 response body `{ "error": "todo not found" }` is written in exactly one place in `src/app.ts`
- [ ] All existing tests pass without being changed
- [ ] A non-numeric id such as `/todos/abc` returns 404 on all four routes, covered by a test

## Risk
🟢 **Low** · no behaviour change, covered by existing tests

## Blocked by
- #3 — touches the same toggle route; build after the reopen fix to avoid a conflict
