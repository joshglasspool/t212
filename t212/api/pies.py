from __future__ import annotations

import warnings

from .._base import APIResponse, _parse_rate_limit
from ..models.pies import (
    AccountBucketInstrumentsDetailedResponse,
    AccountBucketResultResponse,
    DuplicateBucketRequest,
    PieRequest,
)
from ._resource import AsyncResource, SyncResource

_BASE_PATH = "/api/v0/equity/pies"

_DEPRECATION_MSG = (
    "The pies API is deprecated. Pie management via the Trading 212 Public API "
    "is no longer recommended."
)


def _warn() -> None:
    warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=3)


class PiesResource(SyncResource):
    def list(self) -> APIResponse[list[AccountBucketResultResponse]]:
        _warn()
        response = self._engine.get(_BASE_PATH)
        pies = [AccountBucketResultResponse.model_validate(item) for item in response.json()]
        return APIResponse(
            data=pies,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    def get(self, pie_id: int) -> APIResponse[AccountBucketInstrumentsDetailedResponse]:
        _warn()
        response = self._engine.get(f"{_BASE_PATH}/{pie_id}")
        return APIResponse(
            data=AccountBucketInstrumentsDetailedResponse.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    def create(self, request: PieRequest) -> APIResponse[AccountBucketInstrumentsDetailedResponse]:
        _warn()
        response = self._engine.post(
            _BASE_PATH,
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        return APIResponse(
            data=AccountBucketInstrumentsDetailedResponse.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    def update(
        self, pie_id: int, request: PieRequest
    ) -> APIResponse[AccountBucketInstrumentsDetailedResponse]:
        _warn()
        response = self._engine.put(
            f"{_BASE_PATH}/{pie_id}",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        return APIResponse(
            data=AccountBucketInstrumentsDetailedResponse.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    def delete(self, pie_id: int) -> APIResponse[None]:
        _warn()
        response = self._engine.delete(f"{_BASE_PATH}/{pie_id}")
        return APIResponse(
            data=None,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    def duplicate(
        self, pie_id: int, request: DuplicateBucketRequest
    ) -> APIResponse[AccountBucketInstrumentsDetailedResponse]:
        _warn()
        response = self._engine.post(
            f"{_BASE_PATH}/{pie_id}/duplicate",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        return APIResponse(
            data=AccountBucketInstrumentsDetailedResponse.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )


class AsyncPiesResource(AsyncResource):
    async def list(self) -> APIResponse[list[AccountBucketResultResponse]]:
        _warn()
        response = await self._engine.get(_BASE_PATH)
        pies = [AccountBucketResultResponse.model_validate(item) for item in response.json()]
        return APIResponse(
            data=pies,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    async def get(self, pie_id: int) -> APIResponse[AccountBucketInstrumentsDetailedResponse]:
        _warn()
        response = await self._engine.get(f"{_BASE_PATH}/{pie_id}")
        return APIResponse(
            data=AccountBucketInstrumentsDetailedResponse.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    async def create(
        self, request: PieRequest
    ) -> APIResponse[AccountBucketInstrumentsDetailedResponse]:
        _warn()
        response = await self._engine.post(
            _BASE_PATH,
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        return APIResponse(
            data=AccountBucketInstrumentsDetailedResponse.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    async def update(
        self, pie_id: int, request: PieRequest
    ) -> APIResponse[AccountBucketInstrumentsDetailedResponse]:
        _warn()
        response = await self._engine.put(
            f"{_BASE_PATH}/{pie_id}",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        return APIResponse(
            data=AccountBucketInstrumentsDetailedResponse.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    async def delete(self, pie_id: int) -> APIResponse[None]:
        _warn()
        response = await self._engine.delete(f"{_BASE_PATH}/{pie_id}")
        return APIResponse(
            data=None,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    async def duplicate(
        self, pie_id: int, request: DuplicateBucketRequest
    ) -> APIResponse[AccountBucketInstrumentsDetailedResponse]:
        _warn()
        response = await self._engine.post(
            f"{_BASE_PATH}/{pie_id}/duplicate",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        return APIResponse(
            data=AccountBucketInstrumentsDetailedResponse.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )
