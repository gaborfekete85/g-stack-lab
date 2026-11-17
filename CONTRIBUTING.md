# Contributing

## Checks before a PR

These three commands must pass before a PR is opened. Run them from the repo root, in this order:

```bash
uv run ruff check .
uv run mypy
uv run pytest -q
```

They are the `verify_commands` in `.g-stack/config.json`.
