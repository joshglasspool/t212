from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ._utils import to_camel
from .enums import (
    FillTradingMethod,
    FillType,
    OrderInitiatedFrom,
    OrderSide,
    OrderStatus,
    OrderStrategy,
    OrderType,
    TaxName,
    TimeValidity,
)
from .instruments import Instrument


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class Tax(_CamelModel):
    charged_at: datetime | None = None
    currency: str | None = None
    name: TaxName | None = None
    quantity: float | None = None


class FillWalletImpact(_CamelModel):
    currency: str | None = None
    fx_rate: float | None = None
    net_value: float | None = None
    realised_profit_loss: float | None = None
    taxes: list[Tax] | None = None


class Fill(_CamelModel):
    filled_at: datetime | None = None
    id: int | None = None
    price: float | None = None
    quantity: float | None = None
    trading_method: FillTradingMethod | None = None
    type: FillType | None = None
    wallet_impact: FillWalletImpact | None = None


class Order(_CamelModel):
    created_at: datetime | None = None
    currency: str | None = None
    extended_hours: bool | None = None
    filled_quantity: float | None = None
    filled_value: float | None = None
    id: int | None = None
    initiated_from: OrderInitiatedFrom | None = None
    instrument: Instrument | None = None
    limit_price: float | None = None
    quantity: float | None = None
    side: OrderSide | None = None
    status: OrderStatus | None = None
    stop_price: float | None = None
    strategy: OrderStrategy | None = None
    ticker: str | None = None
    time_in_force: TimeValidity | None = None
    type: OrderType | None = None
    value: float | None = None


# Request models (sent to the API — camelCase JSON)
class MarketOrderRequest(_CamelModel):
    ticker: str
    quantity: float
    extended_hours: bool = False


class LimitOrderRequest(_CamelModel):
    ticker: str
    quantity: float
    limit_price: float
    time_validity: TimeValidity = TimeValidity.DAY


class StopOrderRequest(_CamelModel):
    ticker: str
    quantity: float
    stop_price: float
    time_validity: TimeValidity = TimeValidity.DAY


class StopLimitOrderRequest(_CamelModel):
    ticker: str
    quantity: float
    limit_price: float
    stop_price: float
    time_validity: TimeValidity = TimeValidity.DAY
