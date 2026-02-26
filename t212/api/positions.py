from __future__ import annotations

from .._base import APIResponse, _parse_rate_limit
from ..models.positions import Position
from ._resource import AsyncResource, SyncResource

_PATH = "/api/v0/equity/positions"


class PositionsResource(SyncResource):
    def get(self) -> APIResponse[list[Position]]:
        response = self._engine.get(_PATH)
        positions = [Position.model_validate(item) for item in response.json()]
        return APIResponse(
            data=positions,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )


class AsyncPositionsResource(AsyncResource):
    async def get(self) -> APIResponse[list[Position]]:
        response = await self._engine.get(_PATH)
        positions = [Position.model_validate(item) for item in response.json()]
        return APIResponse(
            data=positions,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )
