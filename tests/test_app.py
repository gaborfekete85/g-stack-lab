from __future__ import annotations

from fastapi.testclient import TestClient

from lab.app import create_app


def client() -> TestClient:
    return TestClient(create_app())


def test_create_read_list() -> None:
    c = client()
    created = c.post("/todos", json={"title": "  buy milk "})
    assert created.status_code == 201
    assert created.json()["title"] == "buy milk"
    assert c.get("/todos/1").status_code == 200
    assert len(c.get("/todos").json()) == 1


def test_rejects_a_missing_title() -> None:
    c = client()
    assert c.post("/todos", json={}).status_code == 400
    assert c.post("/todos", json={"title": "   "}).status_code == 400
    assert c.post("/todos", content=b"not json").status_code == 400


def test_rejects_an_unknown_status_filter() -> None:
    assert client().get("/todos?status=weird").status_code == 400


def test_toggle_rename_delete() -> None:
    c = client()
    c.post("/todos", json={"title": "a"})
    assert c.post("/todos/1/toggle").json()["done"] is True
    assert c.patch("/todos/1", json={"title": "b"}).json()["title"] == "b"
    assert c.delete("/todos/1").status_code == 204
    assert c.get("/todos/1").status_code == 404


def test_unknown_ids_are_404_on_every_route() -> None:
    c = client()
    assert c.get("/todos/9").status_code == 404
    assert c.post("/todos/9/toggle").status_code == 404
    assert c.patch("/todos/9", json={"title": "x"}).status_code == 404
    assert c.delete("/todos/9").status_code == 404


def test_serves_the_ui() -> None:
    res = client().get("/")
    assert res.status_code == 200
    assert "<title>g-stack lab · todos</title>" in res.text


def test_stats_counts_open_done_and_total() -> None:
    c = client()
    for title in ("a", "b", "c"):
        c.post("/todos", json={"title": title})
    c.post("/todos/2/toggle")
    res = c.get("/todos/stats")
    assert res.status_code == 200
    assert res.json() == {"open": 2, "done": 1, "total": 3}


def test_stats_with_no_todos_is_all_zero() -> None:
    res = client().get("/todos/stats")
    assert res.status_code == 200
    assert res.json() == {"open": 0, "done": 0, "total": 0}


def test_stats_counts_a_reopened_todo_as_open() -> None:
    c = client()
    c.post("/todos", json={"title": "reopened"})
    c.post("/todos", json={"title": "finished"})
    c.post("/todos/1/toggle")
    c.post("/todos/1/toggle")
    c.post("/todos/2/toggle")
    assert c.get("/todos/stats").json() == {"open": 1, "done": 1, "total": 2}
