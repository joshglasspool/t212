from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any, TypeVar

from pydantic import BaseModel

from ._base import _AsyncHttpEngine, _HttpEngine

T = TypeVar("T", bound=BaseModel)


def paginate_sync(
    engine: _HttpEngine,
    path: str,
    item_type: type[T],
    params: dict[str, Any] | None = None,
) -> Iterator[T]:
    """Iterate over all pages of a cursor-paginated endpoint, yielding individual items."""
    next_path: str | None = path
    query: dict[str, Any] | None = params

    while next_path is not None:
        response = engine.get(next_path, params=query)
        data = response.json()
        query = None  # subsequent requests use the full nextPagePath (no extra params)

        items = data.get("items") or []
        for raw in items:
            yield item_type.model_validate(raw)

        next_page_path: str | None = data.get("nextPagePath")
        next_path = next_page_path


async def paginate_async(
    engine: _AsyncHttpEngine,
    path: str,
    item_type: type[T],
    params: dict[str, Any] | None = None,
) -> AsyncIterator[T]:
    """Async-iterate over all pages of a cursor-paginated endpoint, yielding individual items."""
    next_path: str | None = path
    query: dict[str, Any] | None = params

    while next_path is not None:
        response = await engine.get(next_path, params=query)
        data = response.json()
        query = None

        items = data.get("items") or []
        for raw in items:
            yield item_type.model_validate(raw)

        next_page_path: str | None = data.get("nextPagePath")
        next_path = next_page_path
