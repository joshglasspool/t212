"""Integration-style tests using pytest-httpx to mock HTTP calls."""
import pytest
from pytest_httpx import HTTPXMock

from t212 import Environment, Trading212Client
from t212.models.enums import OrderStatus, OrderType, TimeValidity
from t212.models.orders import LimitOrderRequest, MarketOrderRequest

from .conftest import (
    ACCOUNT_SUMMARY_JSON,
    DEMO_URL,
    DIVIDEND_JSON,
    EXCHANGE_JSON,
    HISTORICAL_ORDER_JSON,
    INSTRUMENT_JSON,
    ORDER_JSON,
    POSITION_JSON,
    RATE_LIMIT_HEADERS,
    TRANSACTION_JSON,
)

API_KEY = "test-key"
API_SECRET = "test-secret"


@pytest.fixture
def client() -> Trading212Client:
    return Trading212Client(API_KEY, API_SECRET, env=Environment.DEMO)


class TestAccountResource:
    def test_get_summary(self, client: Trading212Client, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/account/summary",
            json=ACCOUNT_SUMMARY_JSON,
            headers=RATE_LIMIT_HEADERS,
        )
        result = client.account.get_summary()
        assert result.status_code == 200
        assert result.data.currency == "GBP"
        assert result.data.id == 123456
        assert result.data.total_value == 6000.0
        assert result.rate_limit.remaining == 9
        assert result.rate_limit.limit == 10

    def test_get_summary_cash(self, client: Trading212Client, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/account/summary",
            json=ACCOUNT_SUMMARY_JSON,
            headers=RATE_LIMIT_HEADERS,
        )
        result = client.account.get_summary()
        assert result.data.cash is not None
        assert result.data.cash.available_to_trade == 1000.0


class TestInstrumentsResource:
    def test_list_instruments(self, client: Trading212Client, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/metadata/instruments",
            json=[INSTRUMENT_JSON],
            headers=RATE_LIMIT_HEADERS,
        )
        result = client.instruments.list()
        assert result.status_code == 200
        assert len(result.data) == 1
        assert result.data[0].ticker == "AAPL_US_EQ"

    def test_get_exchanges(self, client: Trading212Client, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/metadata/exchanges",
            json=[EXCHANGE_JSON],
            headers=RATE_LIMIT_HEADERS,
        )
        result = client.instruments.get_exchanges()
        assert len(result.data) == 1
        assert result.data[0].name == "NASDAQ"


class TestOrdersResource:
    def test_list_orders(self, client: Trading212Client, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/orders",
            json=[ORDER_JSON],
            headers=RATE_LIMIT_HEADERS,
        )
        result = client.orders.list()
        assert len(result.data) == 1
        assert result.data[0].id == 987654321

    def test_get_order(self, client: Trading212Client, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/orders/987654321",
            json=ORDER_JSON,
            headers=RATE_LIMIT_HEADERS,
        )
        result = client.orders.get(987654321)
        assert result.data.id == 987654321
        assert result.data.status == OrderStatus.NEW

    def test_cancel_order(self, client: Trading212Client, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/orders/987654321",
            status_code=200,
            headers=RATE_LIMIT_HEADERS,
        )
        result = client.orders.cancel(987654321)
        assert result.status_code == 200
        assert result.data is None

    def test_place_market_order(self, client: Trading212Client, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/orders/market",
            json=ORDER_JSON,
            headers=RATE_LIMIT_HEADERS,
        )
        req = MarketOrderRequest(ticker="AAPL_US_EQ", quantity=1.0)
        result = client.orders.place_market(req)
        assert result.data.type == OrderType.MARKET
        assert result.data.ticker == "AAPL_US_EQ"

    def test_place_limit_order(self, client: Trading212Client, httpx_mock: HTTPXMock) -> None:
        limit_order_json = {**ORDER_JSON, "type": "LIMIT", "limitPrice": 150.0}
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/orders/limit",
            json=limit_order_json,
            headers=RATE_LIMIT_HEADERS,
        )
        req = LimitOrderRequest(
            ticker="AAPL_US_EQ", quantity=1.0, limit_price=150.0, time_validity=TimeValidity.DAY
        )
        result = client.orders.place_limit(req)
        assert result.data.type == OrderType.LIMIT


class TestPositionsResource:
    def test_get_positions(self, client: Trading212Client, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/positions",
            json=[POSITION_JSON],
            headers=RATE_LIMIT_HEADERS,
        )
        result = client.positions.get()
        assert len(result.data) == 1
        pos = result.data[0]
        assert pos.quantity == 5.0
        assert pos.average_price_paid == 150.25


class TestHistoryResource:
    def test_get_orders(self, client: Trading212Client, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/history/orders",
            json={"items": [HISTORICAL_ORDER_JSON], "nextPagePath": None},
            headers=RATE_LIMIT_HEADERS,
        )
        result = client.history.get_orders()
        assert result.data.items is not None
        assert len(result.data.items) == 1
        assert result.data.next_page_path is None

    def test_iter_orders_single_page(
        self, client: Trading212Client, httpx_mock: HTTPXMock
    ) -> None:
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/history/orders",
            json={"items": [HISTORICAL_ORDER_JSON], "nextPagePath": None},
            headers=RATE_LIMIT_HEADERS,
        )
        items = list(client.history.iter_orders())
        assert len(items) == 1
        assert items[0].order is not None
        assert items[0].order.ticker == "AAPL_US_EQ"

    def test_iter_orders_multiple_pages(
        self, client: Trading212Client, httpx_mock: HTTPXMock
    ) -> None:
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/history/orders",
            json={
                "items": [HISTORICAL_ORDER_JSON],
                "nextPagePath": "/api/v0/equity/history/orders?limit=1&cursor=999",
            },
            headers=RATE_LIMIT_HEADERS,
        )
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/history/orders?limit=1&cursor=999",
            json={"items": [HISTORICAL_ORDER_JSON], "nextPagePath": None},
            headers=RATE_LIMIT_HEADERS,
        )
        items = list(client.history.iter_orders())
        assert len(items) == 2

    def test_get_dividends(self, client: Trading212Client, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/history/dividends",
            json={"items": [DIVIDEND_JSON], "nextPagePath": None},
            headers=RATE_LIMIT_HEADERS,
        )
        result = client.history.get_dividends()
        assert result.data.items is not None
        assert result.data.items[0].ticker == "AAPL_US_EQ"

    def test_get_transactions(self, client: Trading212Client, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/history/transactions",
            json={"items": [TRANSACTION_JSON], "nextPagePath": None},
            headers=RATE_LIMIT_HEADERS,
        )
        result = client.history.get_transactions()
        assert result.data.items is not None
        assert result.data.items[0].amount == 500.0

    def test_get_reports(self, client: Trading212Client, httpx_mock: HTTPXMock) -> None:
        report_json = {
            "reportId": 42,
            "status": "Finished",
            "downloadLink": "https://example.com/report.csv",
            "dataIncluded": {"includeOrders": True, "includeDividends": False},
            "timeFrom": "2024-01-01T00:00:00Z",
            "timeTo": "2024-01-31T00:00:00Z",
        }
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/history/exports",
            json=[report_json],
            headers=RATE_LIMIT_HEADERS,
        )
        result = client.history.get_reports()
        assert len(result.data) == 1
        assert result.data[0].report_id == 42


class TestErrorHandling:
    def test_auth_error_raises(self, client: Trading212Client, httpx_mock: HTTPXMock) -> None:
        from t212.exceptions import AuthenticationError

        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/account/summary",
            status_code=401,
            text="Bad API key",
        )
        with pytest.raises(AuthenticationError) as exc_info:
            client.account.get_summary()
        assert exc_info.value.status_code == 401

    def test_rate_limit_error_raises(
        self, client: Trading212Client, httpx_mock: HTTPXMock
    ) -> None:
        from t212.exceptions import RateLimitError

        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/account/summary",
            status_code=429,
            text="Limited: 1 / 5s",
        )
        with pytest.raises(RateLimitError) as exc_info:
            client.account.get_summary()
        assert exc_info.value.status_code == 429

    def test_forbidden_error_raises(
        self, client: Trading212Client, httpx_mock: HTTPXMock
    ) -> None:
        from t212.exceptions import ForbiddenError

        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/account/summary",
            status_code=403,
            text="Scope missing",
        )
        with pytest.raises(ForbiddenError):
            client.account.get_summary()


class TestClientContextManager:
    def test_sync_context_manager(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url=f"{DEMO_URL}/api/v0/equity/account/summary",
            json=ACCOUNT_SUMMARY_JSON,
            headers=RATE_LIMIT_HEADERS,
        )
        with Trading212Client(API_KEY, API_SECRET, env=Environment.DEMO) as client:
            result = client.account.get_summary()
            assert result.data.currency == "GBP"
