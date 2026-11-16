// Seeds the lab's GitHub issues from issues/*.md, in file order, so issue numbers match
// the "Blocked by" references inside them. Idempotent: an issue whose title already exists is skipped.
// Usage: bun scripts/seed-issues.ts <owner/repo>

import { readdirSync, readFileSync } from 'node:fs'
import { join } from 'node:path'

const LABELS: Record<string, { color: string; description: string }> = {
  feature: { color: '1f883d', description: 'New behaviour — built first' },
  bug: { color: 'd73a4a', description: 'Something is broken — built first' },
  refactor: { color: '8250df', description: 'Same behaviour, better shape' },
  docs: { color: '0969da', description: 'Docs only' },
  qa: { color: 'fbca04', description: 'Test what exists — skips Building' },
}

const KIND_TO_LABEL: Record<string, string> = { feature: 'feature', bug: 'bug', refactor: 'refactor', docs: 'docs', qa: 'qa' }

const repo = process.argv[2]
if (!repo || !/^[\w.-]+\/[\w.-]+$/.test(repo)) {
  console.error('usage: bun scripts/seed-issues.ts <owner/repo>')
  process.exit(2)
}

function gh(args: string[]): string {
  const p = Bun.spawnSync(['gh', ...args], { stdout: 'pipe', stderr: 'pipe' })
  if (p.exitCode !== 0) throw new Error(`gh ${args.join(' ')}\n${p.stderr.toString()}`)
  return p.stdout.toString()
}

for (const [name, { color, description }] of Object.entries(LABELS)) {
  gh(['label', 'create', name, '-R', repo, '--color', color, '--description', description, '--force'])
}

const existing = new Set(
  (JSON.parse(gh(['issue', 'list', '-R', repo, '--state', 'all', '--limit', '200', '--json', 'title'])) as { title: string }[]).map(
    (i) => i.title,
  ),
)

const dir = join(import.meta.dir, '..', 'issues')
for (const file of readdirSync(dir).filter((f) => f.endsWith('.md')).sort()) {
  const [first, ...rest] = readFileSync(join(dir, file), 'utf8').split('\n')
  const title = first?.replace(/^#\s+/, '').trim()
  if (!title) throw new Error(`${file}: first line must be "# <title>"`)
  if (existing.has(title)) {
    console.log(`= ${file} already exists`)
    continue
  }
  const kind = title.match(/\[([a-z-]+)\]/)?.[1] ?? ''
  const label = KIND_TO_LABEL[kind]
  const url = gh(['issue', 'create', '-R', repo, '--title', title, '--body', rest.join('\n').trim(), ...(label ? ['--label', label] : [])])
  console.log(`+ ${file} → ${url.trim()}`)
}
