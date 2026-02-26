"""Unit tests for Pydantic model validation."""
from datetime import datetime

from t212.models.account import AccountSummary
from t212.models.enums import (
    DividendType,
    Environment,
    FillTradingMethod,
    FillType,
    InstrumentType,
    OrderInitiatedFrom,
    OrderSide,
    OrderStatus,
    OrderStrategy,
    OrderType,
    TimeEventType,
    TransactionType,
)
from t212.models.history import HistoricalOrder, HistoryDividendItem, HistoryTransactionItem
from t212.models.instruments import Exchange, Instrument, TradableInstrument
from t212.models.orders import MarketOrderRequest, Order
from t212.models.pagination import PaginatedResponse
from t212.models.positions import Position

from .conftest import (
    ACCOUNT_SUMMARY_JSON,
    DIVIDEND_JSON,
    EXCHANGE_JSON,
    HISTORICAL_ORDER_JSON,
    INSTRUMENT_JSON,
    ORDER_JSON,
    POSITION_JSON,
    TRANSACTION_JSON,
)


class TestAccountModels:
    def test_account_summary_parses_camel_case(self) -> None:
        summary = AccountSummary.model_validate(ACCOUNT_SUMMARY_JSON)
        assert summary.currency == "GBP"
        assert summary.id == 123456
        assert summary.total_value == 6000.0

    def test_cash_fields(self) -> None:
        summary = AccountSummary.model_validate(ACCOUNT_SUMMARY_JSON)
        assert summary.cash is not None
        assert summary.cash.available_to_trade == 1000.0
        assert summary.cash.in_pies == 50.0
        assert summary.cash.reserved_for_orders == 100.0

    def test_investments_fields(self) -> None:
        summary = AccountSummary.model_validate(ACCOUNT_SUMMARY_JSON)
        assert summary.investments is not None
        assert summary.investments.current_value == 5000.0
        assert summary.investments.realized_profit_loss == 200.0
        assert summary.investments.total_cost == 4800.0
        assert summary.investments.unrealized_profit_loss == 200.0

    def test_account_summary_all_none(self) -> None:
        summary = AccountSummary.model_validate({})
        assert summary.currency is None
        assert summary.cash is None


class TestInstrumentModels:
    def test_instrument_parses(self) -> None:
        data = {
            "currency": "USD",
            "isin": "US0378331005",
            "name": "Apple Inc.",
            "ticker": "AAPL_US_EQ",
        }
        inst = Instrument.model_validate(data)
        assert inst.ticker == "AAPL_US_EQ"
        assert inst.currency == "USD"

    def test_tradable_instrument(self) -> None:
        inst = TradableInstrument.model_validate(INSTRUMENT_JSON)
        assert inst.ticker == "AAPL_US_EQ"
        assert inst.type == InstrumentType.STOCK
        assert inst.currency_code == "USD"
        assert inst.extended_hours is True

    def test_exchange_with_working_schedules(self) -> None:
        exchange = Exchange.model_validate(EXCHANGE_JSON)
        assert exchange.name == "NASDAQ"
        assert exchange.working_schedules is not None
        assert len(exchange.working_schedules) == 1
        schedule = exchange.working_schedules[0]
        assert schedule.time_events is not None
        assert len(schedule.time_events) == 2
        assert schedule.time_events[0].type == TimeEventType.OPEN
        assert schedule.time_events[1].type == TimeEventType.CLOSE


class TestOrderModels:
    def test_order_parses(self) -> None:
        order = Order.model_validate(ORDER_JSON)
        assert order.id == 987654321
        assert order.ticker == "AAPL_US_EQ"
        assert order.type == OrderType.MARKET
        assert order.side == OrderSide.BUY
        assert order.status == OrderStatus.NEW
        assert order.strategy == OrderStrategy.QUANTITY
        assert order.initiated_from == OrderInitiatedFrom.API
        assert order.quantity == 1.0
        assert isinstance(order.created_at, datetime)

    def test_order_instrument_nested(self) -> None:
        order = Order.model_validate(ORDER_JSON)
        assert order.instrument is not None
        assert order.instrument.ticker == "AAPL_US_EQ"

    def test_market_order_request_serializes(self) -> None:
        req = MarketOrderRequest(ticker="AAPL_US_EQ", quantity=1.0)
        data = req.model_dump(by_alias=True, exclude_none=True)
        assert data["ticker"] == "AAPL_US_EQ"
        assert data["quantity"] == 1.0
        assert data["extendedHours"] is False

    def test_fill_parses(self) -> None:
        hist = HistoricalOrder.model_validate(HISTORICAL_ORDER_JSON)
        assert hist.fill is not None
        assert hist.fill.price == 175.50
        assert hist.fill.trading_method == FillTradingMethod.OTC
        assert hist.fill.type == FillType.TRADE
        assert hist.fill.wallet_impact is not None
        assert hist.fill.wallet_impact.realised_profit_loss == 0.0


class TestPositionModels:
    def test_position_parses(self) -> None:
        pos = Position.model_validate(POSITION_JSON)
        assert pos.quantity == 5.0
        assert pos.average_price_paid == 150.25
        assert pos.current_price == 175.50
        assert pos.quantity_available_for_trading == 5.0
        assert pos.quantity_in_pies == 0.0

    def test_position_wallet_impact(self) -> None:
        pos = Position.model_validate(POSITION_JSON)
        assert pos.wallet_impact is not None
        assert pos.wallet_impact.currency == "GBP"
        assert pos.wallet_impact.unrealized_profit_loss == 126.25


class TestHistoryModels:
    def test_dividend_parses(self) -> None:
        div = HistoryDividendItem.model_validate(DIVIDEND_JSON)
        assert div.ticker == "AAPL_US_EQ"
        assert div.amount == 12.50
        assert div.type == DividendType.ORDINARY
        assert isinstance(div.paid_on, datetime)

    def test_transaction_parses(self) -> None:
        tx = HistoryTransactionItem.model_validate(TRANSACTION_JSON)
        assert tx.amount == 500.0
        assert tx.currency == "GBP"
        assert tx.type == TransactionType.DEPOSIT
        assert isinstance(tx.date_time, datetime)


class TestPaginationModel:
    def test_paginated_response(self) -> None:
        data = {
            "items": [ORDER_JSON, ORDER_JSON],
            "nextPagePath": "/api/v0/equity/history/orders?limit=2&cursor=123",
        }
        page = PaginatedResponse[Order].model_validate(data)
        assert page.next_page_path is not None
        assert "cursor=123" in page.next_page_path
        assert page.items is not None
        assert len(page.items) == 2
        assert page.items[0].ticker == "AAPL_US_EQ"

    def test_paginated_response_no_next(self) -> None:
        data = {"items": [], "nextPagePath": None}
        page = PaginatedResponse[Order].model_validate(data)
        assert page.next_page_path is None
        assert page.items == []


class TestEnums:
    def test_environment_values(self) -> None:
        assert Environment.DEMO == "demo"
        assert Environment.LIVE == "live"

    def test_order_status_values(self) -> None:
        assert OrderStatus.PARTIALLY_FILLED == "PARTIALLY_FILLED"
        assert OrderStatus.FILLED == "FILLED"
