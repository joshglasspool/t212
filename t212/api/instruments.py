from __future__ import annotations

from .._base import APIResponse, _parse_rate_limit
from ..models.instruments import Exchange, TradableInstrument
from ._resource import AsyncResource, SyncResource

_INSTRUMENTS_PATH = "/api/v0/equity/metadata/instruments"
_EXCHANGES_PATH = "/api/v0/equity/metadata/exchanges"


class InstrumentsResource(SyncResource):
    def list(self) -> APIResponse[list[TradableInstrument]]:
        response = self._engine.get(_INSTRUMENTS_PATH)
        instruments = [TradableInstrument.model_validate(item) for item in response.json()]
        return APIResponse(
            data=instruments,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    def get_exchanges(self) -> APIResponse[list[Exchange]]:
        response = self._engine.get(_EXCHANGES_PATH)
        exchanges = [Exchange.model_validate(item) for item in response.json()]
        return APIResponse(
            data=exchanges,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )


class AsyncInstrumentsResource(AsyncResource):
    async def list(self) -> APIResponse[list[TradableInstrument]]:
        response = await self._engine.get(_INSTRUMENTS_PATH)
        instruments = [TradableInstrument.model_validate(item) for item in response.json()]
        return APIResponse(
            data=instruments,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    async def get_exchanges(self) -> APIResponse[list[Exchange]]:
        response = await self._engine.get(_EXCHANGES_PATH)
        exchanges = [Exchange.model_validate(item) for item in response.json()]
        return APIResponse(
            data=exchanges,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )
