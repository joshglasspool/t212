from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ._utils import to_camel
from .instruments import Instrument


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class PositionWalletImpact(_CamelModel):
    currency: str | None = None
    current_value: float | None = None
    fx_impact: float | None = None
    total_cost: float | None = None
    unrealized_profit_loss: float | None = None


class Position(_CamelModel):
    average_price_paid: float | None = None
    created_at: datetime | None = None
    current_price: float | None = None
    instrument: Instrument | None = None
    quantity: float | None = None
    quantity_available_for_trading: float | None = None
    quantity_in_pies: float | None = None
    wallet_impact: PositionWalletImpact | None = None
