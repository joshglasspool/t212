"""Shared fixtures for the t212 test suite."""

DEMO_URL = "https://demo.trading212.com"

RATE_LIMIT_HEADERS = {
    "x-ratelimit-limit": "10",
    "x-ratelimit-period": "60",
    "x-ratelimit-remaining": "9",
    "x-ratelimit-reset": "1700000000",
    "x-ratelimit-used": "1",
}

ACCOUNT_SUMMARY_JSON = {
    "cash": {
        "availableToTrade": 1000.0,
        "inPies": 50.0,
        "reservedForOrders": 100.0,
    },
    "currency": "GBP",
    "id": 123456,
    "investments": {
        "currentValue": 5000.0,
        "realizedProfitLoss": 200.0,
        "totalCost": 4800.0,
        "unrealizedProfitLoss": 200.0,
    },
    "totalValue": 6000.0,
}

ORDER_JSON = {
    "createdAt": "2024-01-15T10:30:00Z",
    "currency": "GBP",
    "extendedHours": False,
    "filledQuantity": 0.0,
    "id": 987654321,
    "initiatedFrom": "API",
    "instrument": {
        "currency": "USD",
        "isin": "US0378331005",
        "name": "Apple Inc.",
        "ticker": "AAPL_US_EQ",
    },
    "quantity": 1.0,
    "side": "BUY",
    "status": "NEW",
    "strategy": "QUANTITY",
    "ticker": "AAPL_US_EQ",
    "type": "MARKET",
}

POSITION_JSON = {
    "averagePricePaid": 150.25,
    "createdAt": "2024-01-10T09:00:00Z",
    "currentPrice": 175.50,
    "instrument": {
        "currency": "USD",
        "isin": "US0378331005",
        "name": "Apple Inc.",
        "ticker": "AAPL_US_EQ",
    },
    "quantity": 5.0,
    "quantityAvailableForTrading": 5.0,
    "quantityInPies": 0.0,
    "walletImpact": {
        "currency": "GBP",
        "currentValue": 877.50,
        "fxImpact": 10.0,
        "totalCost": 751.25,
        "unrealizedProfitLoss": 126.25,
    },
}

HISTORICAL_ORDER_JSON = {
    "order": ORDER_JSON,
    "fill": {
        "filledAt": "2024-01-15T10:30:05Z",
        "id": 111222333,
        "price": 175.50,
        "quantity": 1.0,
        "tradingMethod": "OTC",
        "type": "TRADE",
        "walletImpact": {
            "currency": "GBP",
            "fxRate": 0.79,
            "netValue": -138.65,
            "realisedProfitLoss": 0.0,
            "taxes": [],
        },
    },
}

DIVIDEND_JSON = {
    "amount": 12.50,
    "amountInEuro": 14.30,
    "currency": "GBP",
    "grossAmountPerShare": 0.25,
    "instrument": {
        "currency": "USD",
        "isin": "US0378331005",
        "name": "Apple Inc.",
        "ticker": "AAPL_US_EQ",
    },
    "paidOn": "2024-01-12T00:00:00Z",
    "quantity": 50.0,
    "reference": "DIV-REF-001",
    "ticker": "AAPL_US_EQ",
    "tickerCurrency": "USD",
    "type": "ORDINARY",
}

TRANSACTION_JSON = {
    "amount": 500.0,
    "currency": "GBP",
    "dateTime": "2024-01-05T12:00:00Z",
    "reference": "DEP-REF-001",
    "type": "DEPOSIT",
}

INSTRUMENT_JSON = {
    "addedOn": "2020-01-01T00:00:00Z",
    "currencyCode": "USD",
    "extendedHours": True,
    "isin": "US0378331005",
    "maxOpenQuantity": 10000.0,
    "name": "Apple Inc.",
    "shortName": "AAPL",
    "ticker": "AAPL_US_EQ",
    "type": "STOCK",
    "workingScheduleId": 1,
}

EXCHANGE_JSON = {
    "id": 1,
    "name": "NASDAQ",
    "workingSchedules": [
        {
            "id": 1,
            "timeEvents": [
                {"date": "2024-01-15T14:30:00Z", "type": "OPEN"},
                {"date": "2024-01-15T21:00:00Z", "type": "CLOSE"},
            ],
        }
    ],
}
