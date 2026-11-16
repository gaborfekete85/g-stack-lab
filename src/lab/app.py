from __future__ import annotations

from importlib import metadata
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse

from .store import STATUSES, Store

INDEX_HTML = Path(__file__).parent / "static" / "index.html"
SORTS = ("title",)
ORDERS = ("asc", "desc")


async def _json_body(request: Request) -> dict[str, Any]:
    try:
        body = await request.json()
    except ValueError:
        return {}
    return body if isinstance(body, dict) else {}


def _title(body: dict[str, Any]) -> str | None:
    title = body.get("title")
    return title.strip() if isinstance(title, str) and title.strip() else None


def create_app(store: Store | None = None) -> FastAPI:
    store = store or Store()
    app = FastAPI(title="g-stack-lab")

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        return INDEX_HTML.read_text()

    @app.get("/version")
    def get_version() -> dict[str, str]:
        return {"version": metadata.version("g-stack-lab")}

    @app.get("/todos")
    def list_todos(status: str = "all", sort: str | None = None, order: str | None = None) -> Response:
        if status not in STATUSES:
            return JSONResponse({"error": f"status must be one of {', '.join(STATUSES)}"}, 400)
        if sort is not None and sort not in SORTS:
            return JSONResponse({"error": f"sort must be one of {', '.join(SORTS)}"}, 400)
        if order is not None and sort is None:
            return JSONResponse({"error": "order needs sort"}, 400)
        if order is not None and order not in ORDERS:
            return JSONResponse({"error": f"order must be one of {', '.join(ORDERS)}"}, 400)
        todos = store.list(status)
        if sort == "title":
            todos.sort(key=lambda t: t.title.casefold(), reverse=order == "desc")
        return JSONResponse([t.to_json() for t in todos], headers={"X-Total-Count": str(len(todos))})

    @app.post("/todos")
    async def create_todo(request: Request) -> Response:
        title = _title(await _json_body(request))
        if title is None:
            return JSONResponse({"error": "title is required"}, 400)
        return JSONResponse(store.add(title).to_json(), 201)

    @app.get("/todos/{todo_id}")
    def get_todo(todo_id: int) -> Response:
        todo = store.get(todo_id)
        if todo is None:
            return JSONResponse({"error": "todo not found"}, 404)
        return JSONResponse(todo.to_json())

    @app.post("/todos/{todo_id}/toggle")
    def toggle_todo(todo_id: int) -> Response:
        if store.get(todo_id) is None:
            return JSONResponse({"error": "todo not found"}, 404)
        todo = store.toggle(todo_id)
        assert todo is not None
        return JSONResponse(todo.to_json())

    @app.patch("/todos/{todo_id}")
    async def rename_todo(todo_id: int, request: Request) -> Response:
        if store.get(todo_id) is None:
            return JSONResponse({"error": "todo not found"}, 404)
        title = _title(await _json_body(request))
        if title is None:
            return JSONResponse({"error": "title is required"}, 400)
        todo = store.rename(todo_id, title)
        assert todo is not None
        return JSONResponse(todo.to_json())

    @app.delete("/todos/{todo_id}")
    def delete_todo(todo_id: int) -> Response:
        if store.get(todo_id) is None:
            return JSONResponse({"error": "todo not found"}, 404)
        store.remove(todo_id)
        return Response(status_code=204)

    return app


app = create_app()
