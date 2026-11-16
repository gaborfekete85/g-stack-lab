# ✨ [feature] todos: sort the list by title
## Problem
The list always comes back in creation order; finding a todo in a long list is slow.

## Context
- **Where:** `GET /todos?sort=title`
  - a. Create "banana", "Apple", "cherry"
  - b. Send `GET /todos?sort=title`
- **Who:** API clients and the web UI

## Fix
Add a `sort` parameter; `title` sorts case-insensitively.

## Acceptance Criteria
- [ ] With "banana", "Apple", "cherry", `GET /todos?sort=title` returns titles `["Apple", "banana", "cherry"]`
- [ ] Without `sort`, the order stays creation order
- [ ] `GET /todos?sort=size` returns 400 with `{"error": "sort must be one of title"}`

## Risk
🟢 **Low** · read-only parameter

## Blocked by
- None.
