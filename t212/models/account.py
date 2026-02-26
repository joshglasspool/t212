from pydantic import BaseModel, ConfigDict

from ._utils import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class Cash(_CamelModel):
    available_to_trade: float | None = None
    in_pies: float | None = None
    reserved_for_orders: float | None = None


class Investments(_CamelModel):
    current_value: float | None = None
    realized_profit_loss: float | None = None
    total_cost: float | None = None
    unrealized_profit_loss: float | None = None


class AccountSummary(_CamelModel):
    cash: Cash | None = None
    currency: str | None = None
    id: int | None = None
    investments: Investments | None = None
    total_value: float | None = None
