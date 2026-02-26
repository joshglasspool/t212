from __future__ import annotations

from typing import Any

from ._base import _AsyncHttpEngine, _HttpEngine
from .api.account import AccountResource, AsyncAccountResource
from .api.history import AsyncHistoryResource, HistoryResource
from .api.instruments import AsyncInstrumentsResource, InstrumentsResource
from .api.orders import AsyncOrdersResource, OrdersResource
from .api.pies import AsyncPiesResource, PiesResource
from .api.positions import AsyncPositionsResource, PositionsResource
from .models.enums import Environment


class Trading212Client:
    """Synchronous client for the Trading 212 Public API.

    Usage::

        with Trading212Client("key", "secret", env=Environment.LIVE) as client:
            summary = client.account.get_summary()
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        env: Environment = Environment.DEMO,
        **httpx_kwargs: Any,
    ) -> None:
        self._engine = _HttpEngine(api_key, api_secret, env=env, **httpx_kwargs)
        self.account = AccountResource(self._engine)
        self.instruments = InstrumentsResource(self._engine)
        self.orders = OrdersResource(self._engine)
        self.positions = PositionsResource(self._engine)
        self.history = HistoryResource(self._engine)
        self.pies = PiesResource(self._engine)

    def close(self) -> None:
        self._engine.close()

    def __enter__(self) -> Trading212Client:
        return self

    def __exit__(self, *_args: Any) -> None:
        self.close()


class AsyncTrading212Client:
    """Asynchronous client for the Trading 212 Public API.

    Usage::

        async with AsyncTrading212Client("key", "secret", env=Environment.LIVE) as client:
            summary = await client.account.get_summary()
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        env: Environment = Environment.DEMO,
        **httpx_kwargs: Any,
    ) -> None:
        self._engine = _AsyncHttpEngine(api_key, api_secret, env=env, **httpx_kwargs)
        self.account = AsyncAccountResource(self._engine)
        self.instruments = AsyncInstrumentsResource(self._engine)
        self.orders = AsyncOrdersResource(self._engine)
        self.positions = AsyncPositionsResource(self._engine)
        self.history = AsyncHistoryResource(self._engine)
        self.pies = AsyncPiesResource(self._engine)

    async def aclose(self) -> None:
        await self._engine.aclose()

    async def __aenter__(self) -> AsyncTrading212Client:
        return self

    async def __aexit__(self, *_args: Any) -> None:
        await self.aclose()
