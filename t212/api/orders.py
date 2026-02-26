from __future__ import annotations

from .._base import APIResponse, _parse_rate_limit
from ..models.orders import (
    LimitOrderRequest,
    MarketOrderRequest,
    Order,
    StopLimitOrderRequest,
    StopOrderRequest,
)
from ._resource import AsyncResource, SyncResource

_BASE_PATH = "/api/v0/equity/orders"


class OrdersResource(SyncResource):
    def list(self) -> APIResponse[list[Order]]:
        response = self._engine.get(_BASE_PATH)
        orders = [Order.model_validate(item) for item in response.json()]
        return APIResponse(
            data=orders,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    def get(self, order_id: int) -> APIResponse[Order]:
        response = self._engine.get(f"{_BASE_PATH}/{order_id}")
        return APIResponse(
            data=Order.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    def cancel(self, order_id: int) -> APIResponse[None]:
        response = self._engine.delete(f"{_BASE_PATH}/{order_id}")
        return APIResponse(
            data=None,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    def place_market(self, request: MarketOrderRequest) -> APIResponse[Order]:
        response = self._engine.post(
            f"{_BASE_PATH}/market",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        return APIResponse(
            data=Order.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    def place_limit(self, request: LimitOrderRequest) -> APIResponse[Order]:
        response = self._engine.post(
            f"{_BASE_PATH}/limit",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        return APIResponse(
            data=Order.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    def place_stop(self, request: StopOrderRequest) -> APIResponse[Order]:
        response = self._engine.post(
            f"{_BASE_PATH}/stop",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        return APIResponse(
            data=Order.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    def place_stop_limit(self, request: StopLimitOrderRequest) -> APIResponse[Order]:
        response = self._engine.post(
            f"{_BASE_PATH}/stop_limit",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        return APIResponse(
            data=Order.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )


class AsyncOrdersResource(AsyncResource):
    async def list(self) -> APIResponse[list[Order]]:
        response = await self._engine.get(_BASE_PATH)
        orders = [Order.model_validate(item) for item in response.json()]
        return APIResponse(
            data=orders,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    async def get(self, order_id: int) -> APIResponse[Order]:
        response = await self._engine.get(f"{_BASE_PATH}/{order_id}")
        return APIResponse(
            data=Order.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    async def cancel(self, order_id: int) -> APIResponse[None]:
        response = await self._engine.delete(f"{_BASE_PATH}/{order_id}")
        return APIResponse(
            data=None,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    async def place_market(self, request: MarketOrderRequest) -> APIResponse[Order]:
        response = await self._engine.post(
            f"{_BASE_PATH}/market",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        return APIResponse(
            data=Order.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    async def place_limit(self, request: LimitOrderRequest) -> APIResponse[Order]:
        response = await self._engine.post(
            f"{_BASE_PATH}/limit",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        return APIResponse(
            data=Order.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    async def place_stop(self, request: StopOrderRequest) -> APIResponse[Order]:
        response = await self._engine.post(
            f"{_BASE_PATH}/stop",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        return APIResponse(
            data=Order.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    async def place_stop_limit(self, request: StopLimitOrderRequest) -> APIResponse[Order]:
        response = await self._engine.post(
            f"{_BASE_PATH}/stop_limit",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        return APIResponse(
            data=Order.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )
