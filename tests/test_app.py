from __future__ import annotations

import tomllib
from importlib import metadata
from pathlib import Path

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


TOO_LONG = {"error": "title must be at most 200 characters"}


def test_create_rejects_a_201_character_title_and_creates_nothing() -> None:
    c = client()
    res = c.post("/todos", json={"title": "a" * 201})
    assert res.status_code == 400
    assert res.json() == TOO_LONG
    assert c.get("/todos").json() == []


def test_create_accepts_a_200_character_title() -> None:
    res = client().post("/todos", json={"title": "a" * 200})
    assert res.status_code == 201
    assert res.json()["title"] == "a" * 200


def test_rename_rejects_a_201_character_title_and_keeps_the_old_one() -> None:
    c = client()
    c.post("/todos", json={"title": "old"})
    res = c.patch("/todos/1", json={"title": "b" * 201})
    assert res.status_code == 400
    assert res.json() == TOO_LONG
    assert c.get("/todos/1").json()["title"] == "old"
    assert c.patch("/todos/1", json={"title": "b" * 200}).json()["title"] == "b" * 200


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


def test_version_returns_the_pyproject_version() -> None:
    pyproject = tomllib.loads((Path(__file__).parents[1] / "pyproject.toml").read_text())
    res = client().get("/version")
    assert res.status_code == 200
    assert res.json() == {"version": pyproject["project"]["version"]}


def test_version_follows_the_package_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    for fake in ("9.9.9", "0.2.0rc1"):
        monkeypatch.setattr(metadata, "version", {"g-stack-lab": fake}.__getitem__)
        res = client().get("/version")
        assert res.status_code == 200
        assert res.json() == {"version": fake}
