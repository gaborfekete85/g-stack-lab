export type Todo = {
  id: number
  title: string
  done: boolean
  createdAt: string
  completedAt: string | null
}

export type StatusFilter = 'all' | 'open' | 'done'

export function createStore(now: () => Date = () => new Date()) {
  const todos = new Map<number, Todo>()
  let nextId = 1

  return {
    add(title: string): Todo {
      const todo: Todo = { id: nextId++, title, done: false, createdAt: now().toISOString(), completedAt: null }
      todos.set(todo.id, todo)
      return todo
    },

    get(id: number): Todo | undefined {
      return todos.get(id)
    },

    list(status: StatusFilter = 'all'): Todo[] {
      const all = [...todos.values()]
      if (status === 'open') return all.filter((t) => t.completedAt === null)
      if (status === 'done') return all.filter((t) => t.done)
      return all
    },

    toggle(id: number): Todo | undefined {
      const todo = todos.get(id)
      if (!todo) return undefined
      todo.done = !todo.done
      if (todo.done) todo.completedAt = now().toISOString()
      return todo
    },

    rename(id: number, title: string): Todo | undefined {
      const todo = todos.get(id)
      if (!todo) return undefined
      todo.title = title
      return todo
    },

    remove(id: number): boolean {
      return todos.delete(id)
    },
  }
}

export type Store = ReturnType<typeof createStore>
