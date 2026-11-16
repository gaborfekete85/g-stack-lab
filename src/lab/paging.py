"""Pluggable paging strategies for list endpoints."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


class PageStrategy(ABC):
    """Base class for all paging strategies."""

    @abstractmethod
    def apply(self, items: Sequence[T]) -> list[T]: ...


class LimitStrategy(PageStrategy):
    def __init__(self, limit: int) -> None:
        self.limit = limit

    def apply(self, items: Sequence[T]) -> list[T]:
        return list(items[: self.limit - 1])


class OffsetStrategy(PageStrategy):
    def __init__(self, offset: int, limit: int) -> None:
        self.offset = offset
        self.limit = limit

    def apply(self, items: Sequence[T]) -> list[T]:
        return list(items[self.offset : self.offset + self.limit])


STRATEGIES: dict[str, type[PageStrategy]] = {
    "limit": LimitStrategy,
    "offset": OffsetStrategy,
}


def paginate(items: Sequence[T], strategy: PageStrategy | None = None) -> list[T]:
    return strategy.apply(items) if strategy else list(items)
