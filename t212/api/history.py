from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

from .._base import APIResponse, _parse_rate_limit
from .._pagination import paginate_async, paginate_sync
from ..models.history import (
    EnqueuedReportResponse,
    HistoricalOrder,
    HistoryDividendItem,
    HistoryTransactionItem,
    PublicReportRequest,
    ReportResponse,
)
from ..models.pagination import PaginatedResponse
from ._resource import AsyncResource, SyncResource

_ORDERS_PATH = "/api/v0/equity/history/orders"
_DIVIDENDS_PATH = "/api/v0/equity/history/dividends"
_TRANSACTIONS_PATH = "/api/v0/equity/history/transactions"
_EXPORTS_PATH = "/api/v0/equity/history/exports"


class HistoryResource(SyncResource):
    def get_orders(
        self,
        cursor: int | None = None,
        ticker: str | None = None,
        limit: int | None = None,
    ) -> APIResponse[PaginatedResponse[HistoricalOrder]]:
        params = _build_params(cursor=cursor, ticker=ticker, limit=limit)
        response = self._engine.get(_ORDERS_PATH, params=params or None)
        page = PaginatedResponse[HistoricalOrder].model_validate(response.json())
        return APIResponse(
            data=page,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    def iter_orders(
        self,
        ticker: str | None = None,
        limit: int | None = None,
    ) -> Iterator[HistoricalOrder]:
        params = _build_params(ticker=ticker, limit=limit)
        yield from paginate_sync(self._engine, _ORDERS_PATH, HistoricalOrder, params or None)

    def get_dividends(
        self,
        cursor: int | None = None,
        ticker: str | None = None,
        limit: int | None = None,
    ) -> APIResponse[PaginatedResponse[HistoryDividendItem]]:
        params = _build_params(cursor=cursor, ticker=ticker, limit=limit)
        response = self._engine.get(_DIVIDENDS_PATH, params=params or None)
        page = PaginatedResponse[HistoryDividendItem].model_validate(response.json())
        return APIResponse(
            data=page,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    def iter_dividends(
        self,
        ticker: str | None = None,
        limit: int | None = None,
    ) -> Iterator[HistoryDividendItem]:
        params = _build_params(ticker=ticker, limit=limit)
        yield from paginate_sync(
            self._engine, _DIVIDENDS_PATH, HistoryDividendItem, params or None
        )

    def get_transactions(
        self,
        cursor: str | None = None,
        time: str | None = None,
        limit: int | None = None,
    ) -> APIResponse[PaginatedResponse[HistoryTransactionItem]]:
        params = _build_params(cursor=cursor, time=time, limit=limit)
        response = self._engine.get(_TRANSACTIONS_PATH, params=params or None)
        page = PaginatedResponse[HistoryTransactionItem].model_validate(response.json())
        return APIResponse(
            data=page,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    def iter_transactions(
        self,
        time: str | None = None,
        limit: int | None = None,
    ) -> Iterator[HistoryTransactionItem]:
        params = _build_params(time=time, limit=limit)
        yield from paginate_sync(
            self._engine, _TRANSACTIONS_PATH, HistoryTransactionItem, params or None
        )

    def get_reports(self) -> APIResponse[list[ReportResponse]]:
        response = self._engine.get(_EXPORTS_PATH)
        reports = [ReportResponse.model_validate(item) for item in response.json()]
        return APIResponse(
            data=reports,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    def request_report(self, request: PublicReportRequest) -> APIResponse[EnqueuedReportResponse]:
        response = self._engine.post(
            _EXPORTS_PATH,
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        return APIResponse(
            data=EnqueuedReportResponse.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )


class AsyncHistoryResource(AsyncResource):
    async def get_orders(
        self,
        cursor: int | None = None,
        ticker: str | None = None,
        limit: int | None = None,
    ) -> APIResponse[PaginatedResponse[HistoricalOrder]]:
        params = _build_params(cursor=cursor, ticker=ticker, limit=limit)
        response = await self._engine.get(_ORDERS_PATH, params=params or None)
        page = PaginatedResponse[HistoricalOrder].model_validate(response.json())
        return APIResponse(
            data=page,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    async def iter_orders(
        self,
        ticker: str | None = None,
        limit: int | None = None,
    ) -> AsyncIterator[HistoricalOrder]:
        params = _build_params(ticker=ticker, limit=limit)
        async for item in paginate_async(
            self._engine, _ORDERS_PATH, HistoricalOrder, params or None
        ):
            yield item

    async def get_dividends(
        self,
        cursor: int | None = None,
        ticker: str | None = None,
        limit: int | None = None,
    ) -> APIResponse[PaginatedResponse[HistoryDividendItem]]:
        params = _build_params(cursor=cursor, ticker=ticker, limit=limit)
        response = await self._engine.get(_DIVIDENDS_PATH, params=params or None)
        page = PaginatedResponse[HistoryDividendItem].model_validate(response.json())
        return APIResponse(
            data=page,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    async def iter_dividends(
        self,
        ticker: str | None = None,
        limit: int | None = None,
    ) -> AsyncIterator[HistoryDividendItem]:
        params = _build_params(ticker=ticker, limit=limit)
        async for item in paginate_async(
            self._engine, _DIVIDENDS_PATH, HistoryDividendItem, params or None
        ):
            yield item

    async def get_transactions(
        self,
        cursor: str | None = None,
        time: str | None = None,
        limit: int | None = None,
    ) -> APIResponse[PaginatedResponse[HistoryTransactionItem]]:
        params = _build_params(cursor=cursor, time=time, limit=limit)
        response = await self._engine.get(_TRANSACTIONS_PATH, params=params or None)
        page = PaginatedResponse[HistoryTransactionItem].model_validate(response.json())
        return APIResponse(
            data=page,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    async def iter_transactions(
        self,
        time: str | None = None,
        limit: int | None = None,
    ) -> AsyncIterator[HistoryTransactionItem]:
        params = _build_params(time=time, limit=limit)
        async for item in paginate_async(
            self._engine, _TRANSACTIONS_PATH, HistoryTransactionItem, params or None
        ):
            yield item

    async def get_reports(self) -> APIResponse[list[ReportResponse]]:
        response = await self._engine.get(_EXPORTS_PATH)
        reports = [ReportResponse.model_validate(item) for item in response.json()]
        return APIResponse(
            data=reports,
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )

    async def request_report(
        self, request: PublicReportRequest
    ) -> APIResponse[EnqueuedReportResponse]:
        response = await self._engine.post(
            _EXPORTS_PATH,
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        return APIResponse(
            data=EnqueuedReportResponse.model_validate(response.json()),
            rate_limit=_parse_rate_limit(response.headers),
            status_code=response.status_code,
        )


def _build_params(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}
