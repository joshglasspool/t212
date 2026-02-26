from __future__ import annotations

from .._base import _AsyncHttpEngine, _HttpEngine


class SyncResource:
    """Base class for synchronous API resources."""

    def __init__(self, engine: _HttpEngine) -> None:
        self._engine = engine


class AsyncResource:
    """Base class for asynchronous API resources."""

    def __init__(self, engine: _AsyncHttpEngine) -> None:
        self._engine = engine
