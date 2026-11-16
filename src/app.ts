import { Hono } from 'hono'
import { createStore, type StatusFilter, type Store } from './store'

const STATUSES: StatusFilter[] = ['all', 'open', 'done']

export function createApp(store: Store = createStore()) {
  const app = new Hono()

  app.get('/', async (c) => c.html(await Bun.file(new URL('../public/index.html', import.meta.url)).text()))

  app.get('/todos', (c) => {
    const status = (c.req.query('status') ?? 'all') as StatusFilter
    if (!STATUSES.includes(status)) return c.json({ error: `status must be one of ${STATUSES.join(', ')}` }, 400)
    return c.json(store.list(status))
  })

  app.post('/todos', async (c) => {
    const body = await c.req.json<{ title?: unknown }>().catch(() => ({}) as { title?: unknown })
    if (typeof body.title !== 'string' || !body.title.trim()) return c.json({ error: 'title is required' }, 400)
    return c.json(store.add(body.title.trim()), 201)
  })

  app.get('/todos/:id', (c) => {
    const todo = store.get(Number(c.req.param('id')))
    if (!todo) return c.json({ error: 'todo not found' }, 404)
    return c.json(todo)
  })

  app.post('/todos/:id/toggle', (c) => {
    const id = Number(c.req.param('id'))
    const existing = store.get(id)
    if (!existing) return c.json({ error: 'todo not found' }, 404)
    return c.json(store.toggle(id))
  })

  app.patch('/todos/:id', async (c) => {
    const id = Number(c.req.param('id'))
    const existing = store.get(id)
    if (!existing) return c.json({ error: 'todo not found' }, 404)
    const body = await c.req.json<{ title?: unknown }>().catch(() => ({}) as { title?: unknown })
    if (typeof body.title !== 'string' || !body.title.trim()) return c.json({ error: 'title is required' }, 400)
    return c.json(store.rename(id, body.title.trim()))
  })

  app.delete('/todos/:id', (c) => {
    const id = Number(c.req.param('id'))
    const existing = store.get(id)
    if (!existing) return c.json({ error: 'todo not found' }, 404)
    store.remove(id)
    return c.body(null, 204)
  })

  return app
}
