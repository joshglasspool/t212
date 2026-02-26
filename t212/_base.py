from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

import httpx

from .exceptions import (
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
)
from .models.enums import Environment

T = TypeVar("T")

_BASE_URLS = {
    Environment.DEMO: "https://demo.trading212.com",
    Environment.LIVE: "https://live.trading212.com",
}


@dataclass(frozen=True)
class RateLimitInfo:
    limit: int | None
    period: int | None
    remaining: int | None
    reset: int | None
    used: int | None


@dataclass(frozen=True)
class APIResponse(Generic[T]):
    data: T
    rate_limit: RateLimitInfo
    status_code: int


def _build_auth_header(api_key: str, api_secret: str) -> str:
    token = base64.b64encode(f"{api_key}:{api_secret}".encode('utf-8')).decode('utf-8')
    return f"Basic {token}"


def _parse_rate_limit(headers: httpx.Headers) -> RateLimitInfo:
    def _int(key: str) -> int | None:
        val = headers.get(key)
        try:
            return int(val) if val is not None else None
        except ValueError:
            return None

    return RateLimitInfo(
        limit=_int("x-ratelimit-limit"),
        period=_int("x-ratelimit-period"),
        remaining=_int("x-ratelimit-remaining"),
        reset=_int("x-ratelimit-reset"),
        used=_int("x-ratelimit-used"),
    )


def _raise_for_status(response: httpx.Response) -> None:
    code = response.status_code
    if code == 200:
        return
    try:
        body = response.text
    except Exception:
        body = ""
    if code == 400:
        raise ValidationError(body, code)
    if code == 401:
        raise AuthenticationError(body, code)
    if code == 403:
        raise ForbiddenError(body, code)
    if code == 404:
        raise NotFoundError(body, code)
    if code == 408:
        raise TimeoutError(body, code)
    if code == 429:
        raise RateLimitError(body, code)
    if code >= 500:
        raise ServerError(body, code)
    response.raise_for_status()


class _HttpEngine:
    """Synchronous HTTP engine backed by httpx."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        env: Environment = Environment.DEMO,
        **httpx_kwargs: Any,
    ) -> None:
        base_url = _BASE_URLS[env]
        self._client = httpx.Client(
            base_url=base_url,
            headers={"Authorization": _build_auth_header(api_key, api_secret)},
            **httpx_kwargs,
        )

    def get(self, path: str, params: dict[str, Any] | None = None) -> httpx.Response:
        response = self._client.get(path, params=params)
        _raise_for_status(response)
        return response

    def post(self, path: str, json: Any = None) -> httpx.Response:
        response = self._client.post(path, json=json)
        _raise_for_status(response)
        return response

    def put(self, path: str, json: Any = None) -> httpx.Response:
        response = self._client.put(path, json=json)
        _raise_for_status(response)
        return response

    def delete(self, path: str) -> httpx.Response:
        response = self._client.delete(path)
        _raise_for_status(response)
        return response

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> _HttpEngine:
        return self

    def __exit__(self, *_args: Any) -> None:
        self.close()


class _AsyncHttpEngine:
    """Asynchronous HTTP engine backed by httpx."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        env: Environment = Environment.DEMO,
        **httpx_kwargs: Any,
    ) -> None:
        base_url = _BASE_URLS[env]
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": _build_auth_header(api_key, api_secret)},
            **httpx_kwargs,
        )

    async def get(self, path: str, params: dict[str, Any] | None = None) -> httpx.Response:
        response = await self._client.get(path, params=params)
        _raise_for_status(response)
        return response

    async def post(self, path: str, json: Any = None) -> httpx.Response:
        response = await self._client.post(path, json=json)
        _raise_for_status(response)
        return response

    async def put(self, path: str, json: Any = None) -> httpx.Response:
        response = await self._client.put(path, json=json)
        _raise_for_status(response)
        return response

    async def delete(self, path: str) -> httpx.Response:
        response = await self._client.delete(path)
        _raise_for_status(response)
        return response

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> _AsyncHttpEngine:
        return self

    async def __aexit__(self, *_args: Any) -> None:
        await self.aclose()
