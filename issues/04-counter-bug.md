# 🐛 [bug] ui: remaining counter ignores checkbox toggles
## Problem
The "(N left)" counter next to the heading stays the same when a todo is checked or unchecked. It only updates when a todo is added or the page reloads.

## Context
- **Where:** web UI, `/`
  - a. Add two todos; counter shows "(2 left)"
  - b. Check one todo
  - c. Look at the counter
- **Who:** every web user

## Evidence
- Saw: counter still shows "(2 left)" after checking one todo
- Expected: "(1 left)"
- Reproduced: Chrome, desktop, 2026-11-16

## Fix
Update the counter whenever the list re-renders after a toggle.

## Acceptance Criteria
- [ ] With two open todos, checking one changes the counter from "(2 left)" to "(1 left)" without a reload
- [ ] Unchecking it again changes the counter back to "(2 left)"
- [ ] Screenshots of the counter before and after a toggle, desktop and mobile width, are attached to the PR

## Risk
🟢 **Low** · inline script in one HTML file

## Blocked by
- None.
