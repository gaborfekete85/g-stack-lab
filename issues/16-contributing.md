# 📝 [docs] contributing: how to run the checks before a PR
## Problem
A new contributor does not know which commands must pass before opening a PR.

## Context
- **Where:** new file `CONTRIBUTING.md`
  - a. Open the repo as a new contributor
  - b. Look for how to run the checks
- **Who:** new contributors

## Fix
Add `CONTRIBUTING.md` that lists the three commands from `.g-stack/config.json` `verify_commands`, in order.

## Acceptance Criteria
- [ ] `CONTRIBUTING.md` exists and contains the lines `uv run ruff check .`, `uv run mypy` and `uv run pytest -q`, in that order
- [ ] `CONTRIBUTING.md` says the three commands must pass before a PR is opened

## Risk
🟢 **Low** · documentation only

## Blocked by
- None.
