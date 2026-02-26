from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ._utils import to_camel
from .enums import DividendCashAction, InstrumentIssueName, IssueSeverity, PieStatus


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class InvestmentResult(_CamelModel):
    price_avg_invested_value: float | None = None
    price_avg_result: float | None = None
    price_avg_result_coef: float | None = None
    price_avg_value: float | None = None


class DividendDetails(_CamelModel):
    gained: float | None = None
    in_cash: float | None = None
    reinvested: float | None = None


class InstrumentIssue(_CamelModel):
    name: InstrumentIssueName | None = None
    severity: IssueSeverity | None = None


class AccountBucketDetailedResponse(_CamelModel):
    creation_date: datetime | None = None
    dividend_cash_action: DividendCashAction | None = None
    end_date: datetime | None = None
    goal: float | None = None
    icon: str | None = None
    id: int | None = None
    initial_investment: float | None = None
    instrument_shares: dict[str, float] | None = None
    name: str | None = None
    public_url: str | None = None


class AccountBucketInstrumentResult(_CamelModel):
    current_share: float | None = None
    expected_share: float | None = None
    issues: list[InstrumentIssue] | None = None
    owned_quantity: float | None = None
    result: InvestmentResult | None = None
    ticker: str | None = None


class AccountBucketInstrumentsDetailedResponse(_CamelModel):
    instruments: list[AccountBucketInstrumentResult] | None = None
    settings: AccountBucketDetailedResponse | None = None


class AccountBucketResultResponse(_CamelModel):
    cash: float | None = None
    dividend_details: DividendDetails | None = None
    id: int | None = None
    progress: float | None = None
    result: InvestmentResult | None = None
    status: PieStatus | None = None


class PieRequest(_CamelModel):
    dividend_cash_action: DividendCashAction | None = None
    end_date: datetime | None = None
    goal: float | None = None
    icon: str | None = None
    instrument_shares: dict[str, float] | None = None
    name: str | None = None


class DuplicateBucketRequest(_CamelModel):
    icon: str | None = None
    name: str | None = None
