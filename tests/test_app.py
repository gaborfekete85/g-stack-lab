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


NOT_FOUND = {"error": "todo not found"}


def test_non_numeric_ids_are_404_on_every_route() -> None:
    c = client()
    c.post("/todos", json={"title": "a"})
    for bad in ("abc", "1.5", "1a", "one"):
        for res in (
            c.get(f"/todos/{bad}"),
            c.post(f"/todos/{bad}/toggle"),
            c.patch(f"/todos/{bad}", json={"title": "x"}),
            c.delete(f"/todos/{bad}"),
        ):
            assert (res.status_code, res.json()) == (404, NOT_FOUND)
    assert c.get("/todos/1").json()["title"] == "a"


def test_unknown_numeric_ids_get_the_same_404_body_on_every_route() -> None:
    c = client()
    for res in (
        c.get("/todos/9"),
        c.post("/todos/9/toggle"),
        c.patch("/todos/9", json={"title": "x"}),
        c.delete("/todos/9"),
    ):
        assert (res.status_code, res.json()) == (404, NOT_FOUND)


def test_the_404_body_is_written_once_in_the_app() -> None:
    source = (Path(__file__).parents[1] / "src" / "lab" / "app.py").read_text()
    assert source.count('"todo not found"') == 1


def test_serves_the_ui() -> None:
    res = client().get("/")
    assert res.status_code == 200
    assert "<title>g-stack lab · todos</title>" in res.text


def three_todos_two_done() -> TestClient:
    c = client()
    for title in ("a", "b", "c"):
        c.post("/todos", json={"title": title})
    c.post("/todos/1/toggle")
    c.post("/todos/3/toggle")
    return c


def test_clear_done_reports_how_many_were_removed() -> None:
    res = three_todos_two_done().delete("/todos?status=done")
    assert res.status_code == 200
    assert res.json() == {"removed": 2}


def test_clear_done_leaves_only_the_open_todo() -> None:
    c = three_todos_two_done()
    c.delete("/todos?status=done")
    assert [t["title"] for t in c.get("/todos").json()] == ["b"]


def test_clear_without_status_done_is_400_and_removes_nothing() -> None:
    c = three_todos_two_done()
    assert c.delete("/todos").status_code == 400
    assert c.delete("/todos?status=open").status_code == 400
    assert len(c.get("/todos").json()) == 3


def test_clear_with_any_other_status_is_400_and_removes_nothing() -> None:
    c = three_todos_two_done()
    for status in ("all", "DONE", "Done", "", "done ", "open"):
        res = c.delete("/todos", params={"status": status})
        assert res.status_code == 400, status
    assert [t["title"] for t in c.get("/todos").json()] == ["a", "b", "c"]


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


def search_client() -> TestClient:
    c = client()
    for title in ("Buy milk", "Call mom", "buy bread"):
        c.post("/todos", json={"title": title})
    return c


def test_q_keeps_titles_containing_it_ignoring_case() -> None:
    assert titles(search_client(), "/todos?q=buy") == ["Buy milk", "buy bread"]


def test_q_combines_with_status() -> None:
    c = search_client()
    ids = {t["title"]: t["id"] for t in c.get("/todos").json()}
    for done_title in ("buy bread", "Call mom"):  # "Call mom" is done but must not match q
        c.post(f"/todos/{ids[done_title]}/toggle")
    assert titles(c, "/todos?q=buy&status=done") == ["buy bread"]


def test_empty_q_returns_the_same_list_as_no_q() -> None:
    c = search_client()
    assert titles(c, "/todos?q=") == titles(c, "/todos") == ["Buy milk", "Call mom", "buy bread"]


def test_q_matches_inside_a_title_not_only_at_the_start() -> None:
    assert titles(search_client(), "/todos?q=uy%20b") == ["buy bread"]
    assert titles(search_client(), "/todos?q=MOM") == ["Call mom"]
