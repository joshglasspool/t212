from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ._utils import to_camel
from .enums import DividendType, ReportStatus, TransactionType
from .instruments import Instrument
from .orders import Fill, Order


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class HistoricalOrder(_CamelModel):
    fill: Fill | None = None
    order: Order | None = None


class HistoryDividendItem(_CamelModel):
    amount: float | None = None
    amount_in_euro: float | None = None
    currency: str | None = None
    gross_amount_per_share: float | None = None
    instrument: Instrument | None = None
    paid_on: datetime | None = None
    quantity: float | None = None
    reference: str | None = None
    ticker: str | None = None
    ticker_currency: str | None = None
    type: DividendType | None = None


class HistoryTransactionItem(_CamelModel):
    amount: float | None = None
    currency: str | None = None
    date_time: datetime | None = None
    reference: str | None = None
    type: TransactionType | None = None


class ReportDataIncluded(_CamelModel):
    include_dividends: bool | None = None
    include_interest: bool | None = None
    include_orders: bool | None = None
    include_transactions: bool | None = None


class PublicReportRequest(_CamelModel):
    data_included: ReportDataIncluded | None = None
    time_from: datetime | None = None
    time_to: datetime | None = None


class ReportResponse(_CamelModel):
    data_included: ReportDataIncluded | None = None
    download_link: str | None = None
    report_id: int | None = None
    status: ReportStatus | None = None
    time_from: datetime | None = None
    time_to: datetime | None = None


class EnqueuedReportResponse(_CamelModel):
    report_id: int | None = None
