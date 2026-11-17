# 📝 [docs] api: one page listing every route
## Problem
The only way to learn the API is to read `src/lab/app.py`.

## Context
- **Where:** new file `docs/api.md`
  - a. Look for a list of the API routes
- **Who:** API clients

## Fix
Add `docs/api.md` with one line per route that `src/lab/app.py` defines on main: method, path, one-sentence purpose.

## Acceptance Criteria
- [ ] `docs/api.md` names every route defined on main, each with its HTTP method and path exactly as in the code
- [ ] `docs/api.md` names no route that the code does not define

## Risk
🟢 **Low** · documentation only

## Blocked by
- None.
