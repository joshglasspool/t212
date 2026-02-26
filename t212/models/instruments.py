from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ._utils import to_camel
from .enums import InstrumentType, TimeEventType


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class Instrument(_CamelModel):
    currency: str | None = None
    isin: str | None = None
    name: str | None = None
    ticker: str | None = None


class TimeEvent(_CamelModel):
    date: datetime | None = None
    type: TimeEventType | None = None


class WorkingSchedule(_CamelModel):
    id: int | None = None
    time_events: list[TimeEvent] | None = None


class Exchange(_CamelModel):
    id: int | None = None
    name: str | None = None
    working_schedules: list[WorkingSchedule] | None = None


class TradableInstrument(_CamelModel):
    added_on: datetime | None = None
    currency_code: str | None = None
    extended_hours: bool | None = None
    isin: str | None = None
    max_open_quantity: float | None = None
    name: str | None = None
    short_name: str | None = None
    ticker: str | None = None
    type: InstrumentType | None = None
    working_schedule_id: int | None = None
