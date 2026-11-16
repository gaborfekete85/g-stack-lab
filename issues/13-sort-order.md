# ✨ [feature] todos: descending order for the sorted list
## Problem
Sorting by title only goes A to Z; there is no way to get Z to A.

## Context
- **Where:** `GET /todos?sort=title&order=desc`
  - a. Create "banana", "Apple", "cherry"
  - b. Send `GET /todos?sort=title&order=desc`
- **Who:** API clients and the web UI

## Fix
Add an `order` parameter (`asc` default, `desc`) that applies to `sort`.

## Acceptance Criteria
- [ ] With "banana", "Apple", "cherry", `GET /todos?sort=title&order=desc` returns titles `["cherry", "banana", "Apple"]`
- [ ] `GET /todos?sort=title&order=asc` returns the same as `sort=title` alone
- [ ] `GET /todos?order=desc` without `sort` returns 400 with `{"error": "order needs sort"}`

## Risk
🟢 **Low** · read-only parameter

## Blocked by
- #18 — builds on the `sort` parameter
