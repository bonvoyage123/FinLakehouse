import pytest

from src.ingestion.api_client import FinancialDataClient


def test_daily_prices_uses_fmp_stable_endpoint_and_parameters(monkeypatch):
    client = FinancialDataClient(
        "https://financialmodelingprep.com/stable/",
        "test-key",
    )
    calls = {}

    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return [{"symbol": "MSFT"}]

    def fake_get(url, params, timeout):
        calls.update(url=url, params=params, timeout=timeout)
        return Response()

    monkeypatch.setattr(client.session, "get", fake_get)

    result = client.get_daily_prices("MSFT", "2026-01-01", "2026-01-31")

    assert result == [{"symbol": "MSFT"}]
    assert calls == {
        "url": "https://financialmodelingprep.com/stable/historical-price-eod/full",
        "params": {
            "apikey": "test-key",
            "symbol": "MSFT",
            "from": "2026-01-01",
            "to": "2026-01-31",
        },
        "timeout": 30,
    }


@pytest.mark.parametrize(
    ("method_name", "endpoint"),
    [
        ("get_company_profile", "profile"),
        ("get_income_statement", "income-statement"),
        ("get_balance_sheet", "balance-sheet-statement"),
        ("get_cash_flow_statement", "cash-flow-statement"),
    ],
)
def test_symbol_endpoints_use_fmp_stable_paths_and_parameters(
    monkeypatch,
    method_name,
    endpoint,
):
    client = FinancialDataClient(
        "https://financialmodelingprep.com/stable",
        "test-key",
    )
    calls = {}

    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return [{"symbol": "AAPL"}]

    def fake_get(url, params, timeout):
        calls.update(url=url, params=params)
        return Response()

    monkeypatch.setattr(client.session, "get", fake_get)

    getattr(client, method_name)("AAPL")

    assert calls["url"] == f"https://financialmodelingprep.com/stable/{endpoint}"
    assert calls["params"] == {"apikey": "test-key", "symbol": "AAPL"}
