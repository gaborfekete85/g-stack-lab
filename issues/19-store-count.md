# ♻️ [refactor] store: count todos without building the list
## Problem
Counting todos builds and copies the whole list first, which every counting caller repeats.

## Context
- **Where:** `src/lab/store.py`, class `Store`
  - a. Call `Store.list(status)` only to take its length
- **Who:** code that counts todos

## Fix
Add `Store.count(status)` returning how many todos match the status filter, without building a list.

## Acceptance Criteria
- [ ] With three todos, one completed, `count("all")` is 3, `count("open")` is 2 and `count("done")` is 1
- [ ] An unknown status raises the same error `Store.list` raises for it
- [ ] `count` gives the same number as `len(list(status))` for every status after add, toggle and delete

## Risk
🟡 **Medium** · new method on the shared store

## Blocked by
- None.
