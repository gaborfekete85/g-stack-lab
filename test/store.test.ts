import { describe, expect, test } from 'bun:test'
import { createStore } from '../src/store'

const fixed = () => new Date('2026-01-01T00:00:00Z')

describe('store', () => {
  test('add assigns increasing ids and starts open', () => {
    const s = createStore(fixed)
    expect(s.add('a')).toMatchObject({ id: 1, title: 'a', done: false, completedAt: null })
    expect(s.add('b').id).toBe(2)
  })

  test('toggle completes a todo and stamps completedAt', () => {
    const s = createStore(fixed)
    const t = s.add('a')
    expect(s.toggle(t.id)).toMatchObject({ done: true, completedAt: '2026-01-01T00:00:00.000Z' })
  })

  test('list filters open and done', () => {
    const s = createStore(fixed)
    s.add('open one')
    const d = s.add('done one')
    s.toggle(d.id)
    expect(s.list('open').map((t) => t.title)).toEqual(['open one'])
    expect(s.list('done').map((t) => t.title)).toEqual(['done one'])
    expect(s.list().length).toBe(2)
  })

  test('rename and remove', () => {
    const s = createStore(fixed)
    const t = s.add('a')
    expect(s.rename(t.id, 'b')?.title).toBe('b')
    expect(s.remove(t.id)).toBe(true)
    expect(s.get(t.id)).toBeUndefined()
    expect(s.toggle(99)).toBeUndefined()
  })
})
