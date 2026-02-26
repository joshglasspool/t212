# t212 — Trading 212 Python Client

A typed Python client for the [Trading 212 Public API](https://t212public-api-docs.redoc.ly/). Supports both synchronous and asynchronous usage, full pagination, and all 18 endpoints across the Account, Instruments, Orders, Positions, History, and Pies domains.

```
pip install t212
```

**Requirements:** Python 3.11+

---

## Table of Contents

- [Authentication](#authentication)
- [Environments](#environments)
- [Quick Start](#quick-start)
- [Async Usage](#async-usage)
- [Resources](#resources)
  - [Account](#account)
  - [Instruments](#instruments)
  - [Orders](#orders)
  - [Positions](#positions)
  - [History](#history)
- [Pagination](#pagination)
- [Rate Limiting](#rate-limiting)
- [Error Handling](#error-handling)
- [Advanced Configuration](#advanced-configuration)
- [Development](#development)
- [License](#license)

---

## Authentication

Trading 212's API uses HTTP Basic Authentication. Your **API key** acts as the username and your **API secret** as the password. Generate these in the Trading 212 app under *Settings → API*.

> **Important:** Keep your credentials out of source code. Use environment variables or a secrets manager.

```python
import os
from t212 import Trading212Client, Environment

client = Trading212Client(
    api_key=os.environ["T212_API_KEY"],
    api_secret=os.environ["T212_API_SECRET"],
    env=Environment.LIVE,
)
```

---

## Environments

| Constant | Description |
|---|---|
| `Environment.DEMO` | Paper trading account (default) |
| `Environment.LIVE` | Real money account |

Always test against `DEMO` first. The demo and live environments have **separate credentials**.

---

## Quick Start

```python
from t212 import Trading212Client, Environment

with Trading212Client("my_key", "my_secret", env=Environment.LIVE) as client:
    # Account summary
    summary = client.account.get_summary()
    print(f"Balance: {summary.data.total_value} {summary.data.currency}")
    print(f"Available to trade: {summary.data.cash.available_to_trade}")

    # Open positions
    positions = client.positions.get()
    for pos in positions.data:
        print(f"{pos.instrument.ticker}: qty={pos.quantity}, P&L={pos.wallet_impact.unrealized_profit_loss}")

    # Place a market order
    from t212.models.orders import MarketOrderRequest
    req = MarketOrderRequest(ticker="AAPL_US_EQ", quantity=1.0)
    order = client.orders.place_market(req)
    print(f"Order {order.data.id} status: {order.data.status}")

    # Iterate all dividend history (auto-paginated)
    for div in client.history.iter_dividends():
        print(f"{div.ticker}: {div.amount} {div.currency} on {div.paid_on}")
```

The client implements `__enter__`/`__exit__` so it can be used as a context manager (recommended) or constructed and closed manually with `client.close()`.

---

## Async Usage

Use `AsyncTrading212Client` for async/await environments (FastAPI, asyncio scripts, etc.).

```python
import asyncio
from t212 import AsyncTrading212Client, Environment

async def main():
    async with AsyncTrading212Client("my_key", "my_secret", env=Environment.LIVE) as client:
        summary = await client.account.get_summary()
        print(summary.data.total_value)

        # Async iteration over paginated history
        async for order in client.history.iter_orders():
            print(order.order.id, order.fill.price if order.fill else "pending")

asyncio.run(main())
```

Every method on `AsyncTrading212Client` is `async`. Async iterators (`iter_orders`, `iter_dividends`, `iter_transactions`) use `async for`.

---

## Resources

All resource methods return an `APIResponse[T]` object:

```python
response = client.account.get_summary()
response.data          # The parsed model (AccountSummary, list[Order], etc.)
response.status_code   # HTTP status code (int)
response.rate_limit    # RateLimitInfo — see Rate Limiting section
```

### Account

```python
summary = client.account.get_summary()
# summary.data → AccountSummary

print(summary.data.currency)                          # "GBP"
print(summary.data.total_value)                       # 6000.0
print(summary.data.cash.available_to_trade)           # 1000.0
print(summary.data.cash.reserved_for_orders)          # 100.0
print(summary.data.investments.current_value)         # 5000.0
print(summary.data.investments.unrealized_profit_loss) # 200.0
```

### Instruments

```python
# List all tradable instruments
instruments = client.instruments.list()
# instruments.data → list[TradableInstrument]

for inst in instruments.data:
    print(inst.ticker, inst.name, inst.type, inst.currency_code)

# Get exchange schedules
exchanges = client.instruments.get_exchanges()
# exchanges.data → list[Exchange]

for exchange in exchanges.data:
    print(exchange.name)
    for schedule in exchange.working_schedules or []:
        for event in schedule.time_events or []:
            print(f"  {event.type}: {event.date}")
```

**TradableInstrument fields:** `ticker`, `name`, `isin`, `currency_code`, `type` (`InstrumentType`), `extended_hours`, `working_schedule_id`, `max_open_quantity`, `short_name`, `added_on`.

### Orders

#### Listing & fetching

```python
# All open orders
orders = client.orders.list()
# orders.data → list[Order]

# Single order by ID
order = client.orders.get(987654321)
# order.data → Order

print(order.data.status)    # OrderStatus.NEW
print(order.data.type)      # OrderType.MARKET
print(order.data.side)      # OrderSide.BUY
print(order.data.quantity)  # 1.0
```

#### Placing orders

```python
from t212.models.orders import (
    MarketOrderRequest,
    LimitOrderRequest,
    StopOrderRequest,
    StopLimitOrderRequest,
)
from t212.models.enums import TimeValidity

# Market order
req = MarketOrderRequest(ticker="AAPL_US_EQ", quantity=1.0)
result = client.orders.place_market(req)

# Market order (extended hours)
req = MarketOrderRequest(ticker="AAPL_US_EQ", quantity=1.0, extended_hours=True)
result = client.orders.place_market(req)

# Limit order
req = LimitOrderRequest(
    ticker="AAPL_US_EQ",
    quantity=1.0,
    limit_price=150.00,
    time_validity=TimeValidity.DAY,       # or TimeValidity.GOOD_TILL_CANCEL
)
result = client.orders.place_limit(req)

# Stop order
req = StopOrderRequest(
    ticker="AAPL_US_EQ",
    quantity=1.0,
    stop_price=140.00,
    time_validity=TimeValidity.DAY,
)
result = client.orders.place_stop(req)

# Stop-limit order
req = StopLimitOrderRequest(
    ticker="AAPL_US_EQ",
    quantity=1.0,
    stop_price=140.00,
    limit_price=138.00,
    time_validity=TimeValidity.GOOD_TILL_CANCEL,
)
result = client.orders.place_stop_limit(req)
```

#### Cancelling

```python
result = client.orders.cancel(987654321)
# result.data is None on success
```

**Order fields:** `id`, `ticker`, `type`, `side`, `status`, `strategy`, `quantity`, `filled_quantity`, `limit_price`, `stop_price`, `time_in_force`, `currency`, `extended_hours`, `initiated_from`, `created_at`, `instrument`.

### Positions

```python
positions = client.positions.get()
# positions.data → list[Position]

for pos in positions.data:
    print(pos.instrument.ticker)
    print(pos.quantity)
    print(pos.average_price_paid)
    print(pos.current_price)
    print(pos.quantity_available_for_trading)
    print(pos.wallet_impact.unrealized_profit_loss)
    print(pos.wallet_impact.currency)
```

**Position fields:** `instrument`, `quantity`, `average_price_paid`, `current_price`, `quantity_available_for_trading`, `quantity_in_pies`, `created_at`, `wallet_impact`.

### History

#### Orders history

```python
# Single page
page = client.history.get_orders(cursor=None, ticker="AAPL_US_EQ", limit=50)
# page.data → PaginatedResponse[HistoricalOrder]
print(page.data.items)         # list[HistoricalOrder]
print(page.data.next_page_path)  # str | None

# Auto-paginate (yields every item across all pages)
for hist_order in client.history.iter_orders(ticker="AAPL_US_EQ"):
    print(hist_order.order.id, hist_order.fill.price if hist_order.fill else None)
```

#### Dividends history

```python
page = client.history.get_dividends(limit=100)
for div in client.history.iter_dividends():
    print(div.ticker, div.amount, div.type, div.paid_on)
```

**HistoryDividendItem fields:** `ticker`, `amount`, `currency`, `gross_amount_per_share`, `quantity`, `paid_on`, `type` (`DividendType`), `reference`, `instrument`.

#### Transactions history

```python
page = client.history.get_transactions(limit=100)
for tx in client.history.iter_transactions():
    print(tx.type, tx.amount, tx.currency, tx.date_time)
```

**TransactionType values:** `DEPOSIT`, `WITHDRAW`, `FEE`, `TRANSFER`.

#### CSV reports

```python
from t212.models.history import PublicReportRequest, ReportDataIncluded

# Request a new report
req = PublicReportRequest(
    data_included=ReportDataIncluded(include_dividends=True, include_orders=True),
    time_from="2024-01-01T00:00:00Z",
    time_to="2024-12-31T23:59:59Z",
)
enqueued = client.history.request_report(req)
print(enqueued.data.report_id)

# Check existing reports
reports = client.history.get_reports()
for r in reports.data:
    print(r.report_id, r.status, r.download_link)
```

---

## Pagination

Endpoints that return lists of historical data are cursor-paginated. You can either manage pages manually or use the `iter_*` convenience methods:

```python
# Manual pagination
cursor = None
while True:
    page = client.history.get_orders(cursor=cursor, limit=50)
    for item in page.data.items or []:
        process(item)
    if page.data.next_page_path is None:
        break
    # Extract cursor from next_page_path for the next call
    import urllib.parse as up
    qs = up.parse_qs(up.urlparse(page.data.next_page_path).query)
    cursor = int(qs["cursor"][0])

# Automatic (recommended)
for item in client.history.iter_orders(limit=50):
    process(item)
```

The `iter_*` methods (`iter_orders`, `iter_dividends`, `iter_transactions`) handle all page fetching automatically and yield items one by one.

---

## Rate Limiting

Every `APIResponse` includes a `rate_limit` attribute:

```python
result = client.account.get_summary()
rl = result.rate_limit

rl.limit      # int | None — requests allowed per period
rl.remaining  # int | None — requests left in current window
rl.used       # int | None — requests used so far
rl.period     # int | None — window length in seconds
rl.reset      # int | None — Unix timestamp when the window resets
```

The client does **not** auto-retry on `429 RateLimitError`. Implement retry logic in your application:

```python
import time
from t212 import RateLimitError

def safe_get_summary(client):
    while True:
        try:
            return client.account.get_summary()
        except RateLimitError as e:
            reset = e.status_code  # use rate_limit.reset from previous response
            time.sleep(5)
```

---

## Error Handling

All exceptions inherit from `Trading212Error` and carry a `.status_code` attribute.

| Exception | HTTP Status | Cause |
|---|---|---|
| `AuthenticationError` | 401 | Invalid API key or secret |
| `ForbiddenError` | 403 | Missing scope or permission |
| `NotFoundError` | 404 | Resource does not exist |
| `ValidationError` | 400 | Bad request / invalid parameters |
| `RateLimitError` | 429 | Rate limit exceeded |
| `TimeoutError` | 408 | Request timed out |
| `ServerError` | 5xx | Trading 212 server error |

```python
from t212 import (
    Trading212Error,
    AuthenticationError,
    RateLimitError,
    ForbiddenError,
)

try:
    result = client.account.get_summary()
except AuthenticationError:
    print("Check your API key and secret")
except ForbiddenError:
    print("Enable the required API scope in the Trading 212 app")
except RateLimitError as e:
    print(f"Rate limited (HTTP {e.status_code}), back off and retry")
except Trading212Error as e:
    print(f"API error {e.status_code}: {e}")
```

---

## Advanced Configuration

The client passes `**httpx_kwargs` directly to the underlying `httpx.Client` / `httpx.AsyncClient`, so you can customise timeouts, proxies, transport, and headers.

```python
import httpx
from t212 import Trading212Client, Environment

# Custom timeout
client = Trading212Client(
    "key", "secret",
    env=Environment.LIVE,
    timeout=httpx.Timeout(30.0, connect=5.0),
)

# HTTP proxy
client = Trading212Client(
    "key", "secret",
    env=Environment.LIVE,
    proxies={"https://": "http://proxy.example.com:8080"},
)

# Custom transport (e.g. for testing)
transport = httpx.MockTransport(...)
client = Trading212Client("key", "secret", transport=transport)
```

---

## Development

```bash
# Clone and install with dev dependencies
git clone https://github.com/jglasspool/t212.git
cd t212
python3.11 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest tests/

# Lint
ruff check t212/

# Type check
mypy t212/
```

Tests use `pytest-httpx` to mock all HTTP calls — no real credentials or network access needed.

The OpenAPI spec the client was built from lives at [`spec/api.yaml`](spec/api.yaml). When Trading 212 publishes an updated spec, diff it against this file to identify endpoints or schema changes that need updating in the client.

---

## License

MIT — see [LICENSE](LICENSE) for details.

This project is an independent open-source library and is **not affiliated with, endorsed by, or supported by Trading 212**. Use of the Trading 212 API is subject to their [Terms of Service](https://www.trading212.com/terms).
