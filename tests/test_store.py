from __future__ import annotations

from datetime import UTC, datetime

from lab.store import Store


def fixed() -> datetime:
    return datetime(2026, 1, 1, tzinfo=UTC)


def test_add_assigns_increasing_ids_and_starts_open() -> None:
    s = Store(fixed)
    first = s.add("a")
    assert (first.id, first.title, first.done, first.completed_at) == (1, "a", False, None)
    assert s.add("b").id == 2


def test_toggle_completes_and_stamps_completed_at() -> None:
    s = Store(fixed)
    todo = s.toggle(s.add("a").id)
    assert todo is not None
    assert (todo.done, todo.completed_at) == (True, "2026-01-01T00:00:00+00:00")


def test_list_filters_open_and_done() -> None:
    s = Store(fixed)
    s.add("open one")
    s.toggle(s.add("done one").id)
    assert [t.title for t in s.list("open")] == ["open one"]
    assert [t.title for t in s.list("done")] == ["done one"]
    assert len(s.list()) == 2


def test_rename_remove_and_unknown_ids() -> None:
    s = Store(fixed)
    todo_id = s.add("a").id
    renamed = s.rename(todo_id, "b")
    assert renamed is not None and renamed.title == "b"
    assert s.remove(todo_id) is True
    assert s.get(todo_id) is None
    assert s.toggle(99) is None
    assert s.remove(99) is False


def reopened() -> tuple[Store, int]:
    s = Store(fixed)
    todo_id = s.add("a").id
    s.toggle(todo_id)
    s.toggle(todo_id)
    return s, todo_id


def test_reopened_todo_is_listed_as_open() -> None:
    s, todo_id = reopened()
    assert [t.id for t in s.list("open")] == [todo_id]


def test_reopened_todo_has_no_completed_at() -> None:
    s, todo_id = reopened()
    todo = s.get(todo_id)
    assert todo is not None
    assert todo.completed_at is None


def test_reopened_todo_is_not_listed_as_done() -> None:
    s, _ = reopened()
    assert s.list("done") == []
