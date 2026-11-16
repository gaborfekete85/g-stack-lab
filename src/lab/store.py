from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any, Literal

StatusFilter = Literal["all", "open", "done"]
STATUSES: tuple[StatusFilter, ...] = ("all", "open", "done")


@dataclass
class Todo:
    id: int
    title: str
    done: bool
    created_at: str
    completed_at: str | None

    def to_json(self) -> dict[str, Any]:
        return asdict(self)


def _utc_now() -> datetime:
    return datetime.now(UTC)


class Store:
    """In-memory todo store."""

    def __init__(self, now: Callable[[], datetime] = _utc_now) -> None:
        self._todos: dict[int, Todo] = {}
        self._next_id = 1
        self._now = now

    def add(self, title: str) -> Todo:
        todo = Todo(self._next_id, title, done=False, created_at=self._now().isoformat(), completed_at=None)
        self._todos[todo.id] = todo
        self._next_id += 1
        return todo

    def get(self, todo_id: int) -> Todo | None:
        return self._todos.get(todo_id)

    def list(self, status: StatusFilter = "all") -> list[Todo]:
        todos = list(self._todos.values())
        if status == "open":
            return [t for t in todos if t.completed_at is None]
        if status == "done":
            return [t for t in todos if t.done]
        return todos

    def toggle(self, todo_id: int) -> Todo | None:
        todo = self._todos.get(todo_id)
        if todo is None:
            return None
        todo.done = not todo.done
        if todo.done:
            todo.completed_at = self._now().isoformat()
        return todo

    def rename(self, todo_id: int, title: str) -> Todo | None:
        todo = self._todos.get(todo_id)
        if todo is None:
            return None
        todo.title = title
        return todo

    def remove(self, todo_id: int) -> bool:
        return self._todos.pop(todo_id, None) is not None
