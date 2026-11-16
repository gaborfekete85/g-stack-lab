# ✨ [feature] app: version endpoint for deploy checks
## Problem
After a deploy there is no way to ask the running app which version it is.

## Context
- **Where:** `GET /version`
  - a. Start the app
  - b. Send `GET /version`
- **Who:** deploy scripts, people debugging a deploy

## Fix
Add `GET /version` that returns the version from the package metadata.

## Acceptance Criteria
- [ ] `GET /version` returns 200 with `{"version": "<the version in pyproject.toml>"}`
- [ ] The version in the response changes when the version in `pyproject.toml` changes (no hard-coded string)

## Risk
🟢 **Low** · new read-only route

## Blocked by
- None.
