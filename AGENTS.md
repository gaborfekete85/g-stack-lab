# g-stack-lab — agent notes

The test bench for g-stack, a personal software factory. A small todo app (bun + Hono + one HTML page). Its issues are seeded on purpose: some are good tickets, one is deliberately vague, two describe real bugs in this code. **Do not fix things outside the ticket you were given.**

## Verify

```bash
bun install
bun run verify     # typecheck + tests; this is the project's verify command
bun run dev        # http://localhost:3000
```

## Layout

| Path | What |
|---|---|
| `src/store.ts` | In-memory todo store |
| `src/app.ts` | Hono routes; `createApp()` is what tests call |
| `src/server.ts` | Starts the server |
| `public/index.html` | The whole UI: markup + inline script |
| `test/` | `bun test`, using `app.request()` — no real server needed |
| `issues/` | Source of the seeded GitHub issues |
| `scripts/seed-issues.ts` | Creates labels and issues on GitHub (idempotent) |

## Conventions

- Commits and PRs follow the g-stack writing standard: `<emoji> [type] scope: subject`.
- Tests live next to the layer the behaviour lives at: store logic → `test/store.test.ts`, routes → `test/app.test.ts`, UI → Playwright (added when needed).
