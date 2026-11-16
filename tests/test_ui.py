from __future__ import annotations

import socket
import threading
from collections.abc import Iterator

import pytest
import uvicorn
from playwright.sync_api import Page, expect, sync_playwright

from lab.app import create_app
from lab.store import Store


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port: int = s.getsockname()[1]
        return port


@pytest.fixture
def page() -> Iterator[Page]:
    """The UI served by a real server with two open todos, "a" and "b"."""
    store = Store()
    store.add("a")
    store.add("b")
    port = _free_port()
    server = uvicorn.Server(uvicorn.Config(create_app(store), host="127.0.0.1", port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    while not server.started:
        threading.Event().wait(0.01)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{port}/")
            expect(page.get_by_test_id("remaining")).to_have_text("(2 left)")
            yield page
            browser.close()
    finally:
        server.should_exit = True
        thread.join()


def test_checking_a_todo_updates_the_remaining_counter(page: Page) -> None:
    page.get_by_label("Toggle a").check()
    expect(page.get_by_test_id("remaining")).to_have_text("(1 left)", timeout=2000)


def test_unchecking_a_todo_restores_the_remaining_counter(page: Page) -> None:
    remaining = page.get_by_test_id("remaining")
    page.get_by_label("Toggle a").check()
    expect(remaining).to_have_text("(1 left)", timeout=2000)
    page.get_by_label("Toggle a").uncheck()
    expect(remaining).to_have_text("(2 left)", timeout=2000)
