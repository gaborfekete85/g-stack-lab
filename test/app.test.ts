import { describe, expect, test } from 'bun:test'
import { createApp } from '../src/app'

const json = (body: unknown) => ({
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify(body),
})

describe('todos API', () => {
  test('create, read, list', async () => {
    const app = createApp()
    const created = await app.request('/todos', json({ title: '  buy milk ' }))
    expect(created.status).toBe(201)
    expect(await created.json()).toMatchObject({ id: 1, title: 'buy milk' })
    expect((await app.request('/todos/1')).status).toBe(200)
    expect(await (await app.request('/todos')).json()).toHaveLength(1)
  })

  test('rejects a missing title', async () => {
    const app = createApp()
    expect((await app.request('/todos', json({}))).status).toBe(400)
    expect((await app.request('/todos', json({ title: '   ' }))).status).toBe(400)
  })

  test('rejects an unknown status filter', async () => {
    expect((await createApp().request('/todos?status=weird')).status).toBe(400)
  })

  test('toggle, rename, delete', async () => {
    const app = createApp()
    await app.request('/todos', json({ title: 'a' }))
    expect(await (await app.request('/todos/1/toggle', { method: 'POST' })).json()).toMatchObject({ done: true })
    const renamed = await app.request('/todos/1', { ...json({ title: 'b' }), method: 'PATCH' })
    expect(await renamed.json()).toMatchObject({ title: 'b' })
    expect((await app.request('/todos/1', { method: 'DELETE' })).status).toBe(204)
    expect((await app.request('/todos/1')).status).toBe(404)
  })

  test('unknown ids are 404 on every route', async () => {
    const app = createApp()
    expect((await app.request('/todos/9')).status).toBe(404)
    expect((await app.request('/todos/9/toggle', { method: 'POST' })).status).toBe(404)
    expect((await app.request('/todos/9', { ...json({ title: 'x' }), method: 'PATCH' })).status).toBe(404)
    expect((await app.request('/todos/9', { method: 'DELETE' })).status).toBe(404)
  })

  test('serves the UI at /', async () => {
    const res = await createApp().request('/')
    expect(res.status).toBe(200)
    expect(await res.text()).toContain('<title>g-stack lab · todos</title>')
  })
})
