from __future__ import annotations

from .._base import APIResponse, _parse_rate_limit
from ..models.account import AccountSummary
from ._resource import AsyncResource, SyncResource

_PATH = "/api/v0/equity/account/summary"


class AccountResource(SyncResource):
    def get_summary(self) -> APIResponse[AccountSummary]:
        response = self._engine.get(_PATH)
        return APIResponse(
            data=AccountSummary.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )


class AsyncAccountResource(AsyncResource):
    async def get_summary(self) -> APIResponse[AccountSummary]:
        response = await self._engine.get(_PATH)
        return APIResponse(
            data=AccountSummary.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )
