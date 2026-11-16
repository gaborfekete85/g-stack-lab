# g-stack-lab — agent notes

The test bench for g-stack, a personal software factory. A small todo app (Python, FastAPI, one HTML page). Its issues are seeded on purpose: some are good tickets, one is deliberately vague, two describe real bugs in this code. **Do not fix things outside the ticket you were given.**

## Verify

```bash
uv sync
uv run ruff check . && uv run mypy && uv run pytest    # the project's verify command
uv run uvicorn lab.app:app --reload                     # http://localhost:8000
```

## Layout

| Path | What |
|---|---|
| `src/lab/store.py` | In-memory todo store |
| `src/lab/app.py` | FastAPI routes; `create_app()` is what tests call |
| `src/lab/static/index.html` | The whole UI: markup + inline script |
| `tests/` | pytest with FastAPI's `TestClient` — no real server needed |
| `issues/` | Source of the seeded GitHub issues |
| `scripts/seed_issues.py` | Creates labels and issues on GitHub (idempotent; `--update` syncs bodies) |

## Conventions

- Python 3.12 via uv. Never call bare `python3` (the system one is 3.9).
- Commits and PRs follow the g-stack writing standard: `<emoji> [type] scope: subject`.
- Tests live at the layer the behaviour lives at: store logic → `tests/test_store.py`, routes → `tests/test_app.py`, UI → Playwright (added when needed).
