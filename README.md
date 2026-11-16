# g-stack-lab

Test bench for g-stack, a personal software factory. A tiny todo app (Python + FastAPI) with seeded issues, used to demo every g-stack version.

```bash
uv sync
uv run ruff check . && uv run mypy && uv run pytest
uv run uvicorn lab.app:app --reload    # http://localhost:8000
```

Seed (or re-sync) the GitHub issues: `uv run python scripts/seed_issues.py <owner/repo> [--update]`.

# race: a late push after the review
