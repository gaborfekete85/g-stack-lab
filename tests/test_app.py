from __future__ import annotations

import pytest
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


def titles(c: TestClient, url: str) -> list[str]:
    return [t["title"] for t in c.get(url).json()]


def test_sort_by_title_is_case_insensitive() -> None:
    c = client()
    for title in ("banana", "Apple", "cherry"):
        c.post("/todos", json={"title": title})
    assert titles(c, "/todos?sort=title") == ["Apple", "banana", "cherry"]

    c = client()
    for title in ("apple", "Cherry", "Banana"):
        c.post("/todos", json={"title": title})
    assert titles(c, "/todos?sort=title") == ["apple", "Banana", "Cherry"]


def test_without_sort_the_list_keeps_creation_order() -> None:
    c = client()
    for title in ("banana", "Apple", "cherry"):
        c.post("/todos", json={"title": title})
    assert titles(c, "/todos") == ["banana", "Apple", "cherry"]


def test_rejects_an_unknown_sort() -> None:
    c = client()
    for sort in ("size", "TITLE"):
        res = c.get(f"/todos?sort={sort}")
        assert res.status_code == 400
        assert res.json() == {"error": "sort must be one of title"}


def test_order_desc_reverses_the_title_sort() -> None:
    c = client()
    for title in ("banana", "Apple", "cherry"):
        c.post("/todos", json={"title": title})
    assert titles(c, "/todos?sort=title&order=desc") == ["cherry", "banana", "Apple"]


def test_order_asc_matches_sort_alone() -> None:
    c = client()
    for title in ("banana", "Apple", "cherry"):
        c.post("/todos", json={"title": title})
    expected = ["Apple", "banana", "cherry"]
    assert titles(c, "/todos?sort=title") == expected
    assert titles(c, "/todos?sort=title&order=asc") == expected


def test_order_without_sort_is_rejected() -> None:
    c = client()
    c.post("/todos", json={"title": "a"})
    for order in ("desc", "asc"):
        res = c.get(f"/todos?order={order}")
        assert res.status_code == 400
        assert res.json() == {"error": "order needs sort"}


def test_rejects_an_unknown_order() -> None:
    c = client()
    for order in ("up", "DESC", ""):
        res = c.get(f"/todos?sort=title&order={order}")
        assert res.status_code == 400
        assert res.json() == {"error": "order must be one of asc, desc"}


ADMIN_DENIED = {"error": "admin token required"}


def admin_client(monkeypatch: pytest.MonkeyPatch, token: str | None, todos: int = 2) -> TestClient:
    if token is None:
        monkeypatch.delenv("LAB_ADMIN_TOKEN", raising=False)
    else:
        monkeypatch.setenv("LAB_ADMIN_TOKEN", token)
    c = client()
    for i in range(todos):
        c.post("/todos", json={"title": f"t{i}"})
    return c


def test_admin_stats_returns_the_total_with_the_right_token(monkeypatch: pytest.MonkeyPatch) -> None:
    c = admin_client(monkeypatch, "s3cret")
    res = c.get("/admin/stats", headers={"X-Admin-Token": "s3cret"})
    assert res.status_code == 200
    assert res.json() == {"total": 2}
    c.post("/todos", json={"title": "third"})
    c.post("/todos/1/toggle")
    assert c.get("/admin/stats", headers={"X-Admin-Token": "s3cret"}).json() == {"total": 3}


@pytest.mark.parametrize(
    "headers", [{"X-Admin-Token": "wrong"}, {"X-Admin-Token": "S3CRET"}, {"X-Admin-Token": ""}, {}]
)
def test_admin_stats_rejects_a_wrong_or_missing_token(monkeypatch: pytest.MonkeyPatch, headers: dict[str, str]) -> None:
    res = admin_client(monkeypatch, "s3cret").get("/admin/stats", headers=headers)
    assert res.status_code == 401
    assert res.json() == ADMIN_DENIED


@pytest.mark.parametrize("env", [None, ""])
@pytest.mark.parametrize("headers", [{"X-Admin-Token": "s3cret"}, {"X-Admin-Token": ""}, {}])
def test_admin_stats_is_closed_without_a_configured_token(
    monkeypatch: pytest.MonkeyPatch, env: str | None, headers: dict[str, str]
) -> None:
    res = admin_client(monkeypatch, env).get("/admin/stats", headers=headers)
    assert res.status_code == 401
    assert res.json() == ADMIN_DENIED
