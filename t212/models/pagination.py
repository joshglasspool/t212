from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

from ._utils import to_camel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    items: list[T] | None = None
    next_page_path: str | None = None
