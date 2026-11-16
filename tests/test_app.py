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


def _three_todos() -> TestClient:
    c = client()
    for title in ("a", "b", "c"):
        c.post("/todos", json={"title": title})
    return c


def _ids(c: TestClient, url: str) -> list[int]:
    return [t["id"] for t in c.get(url).json()]


def test_limit_caps_the_number_of_todos() -> None:
    c = _three_todos()
    assert _ids(c, "/todos?limit=2") == [1, 2]
    assert _ids(c, "/todos?limit=1") == [1]
    assert _ids(c, "/todos?limit=3") == [1, 2, 3]


def test_limit_must_be_positive() -> None:
    c = _three_todos()
    assert c.get("/todos?limit=0").status_code == 400
    assert c.get("/todos?limit=-1").status_code == 400


def test_no_limit_returns_everything() -> None:
    assert _ids(_three_todos(), "/todos") == [1, 2, 3]
