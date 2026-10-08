from types import SimpleNamespace

import pytest

from src.ingestion import fmp_ingestion


def test_ingest_fmp_data_uploads_v1_datasets_to_raw(monkeypatch):
    calls = []

    class FakeClient:
        def __init__(self, base_url, api_key):
            calls.append(("client", base_url, api_key))

        def __getattr__(self, method_name):
            def fetch(symbol):
                calls.append(("fetch", method_name, symbol))
                return {"method": method_name, "symbol": symbol}

            return fetch

    class FakeUploader:
        def __init__(self, bucket, prefix):
            calls.append(("uploader", bucket, prefix))

        def upload_json(self, payload, object_key):
            calls.append(("upload", payload, object_key))
            return f"raw/{object_key}"

    monkeypatch.setattr(
        fmp_ingestion,
        "get_settings",
        lambda: SimpleNamespace(
            fmp_symbols=(" msft ",),
            fmp_api_key="test-key",
            fmp_api_base_url="https://example.test/stable/",
            s3_bucket="test-bucket",
            raw_prefix="raw",
        ),
    )
    monkeypatch.setattr(fmp_ingestion, "FinancialDataClient", FakeClient)
    monkeypatch.setattr(fmp_ingestion, "S3Uploader", FakeUploader)

    uploaded_keys = fmp_ingestion.ingest_fmp_data()

    assert len(uploaded_keys) == 5
    assert [entry[1] for entry in calls if entry[0] == "fetch"] == [
        "get_daily_prices",
        "get_company_profile",
        "get_income_statement",
        "get_balance_sheet",
        "get_cash_flow_statement",
    ]
    assert all("/MSFT.json" in key for key in uploaded_keys)
    assert all(key.startswith("raw/") for key in uploaded_keys)


@pytest.mark.parametrize(
    ("symbols", "api_key", "message"),
    [
        ((), "test-key", "No FMP symbols configured"),
        (("MSFT",), "", "FMP_API_KEY is required"),
    ],
)
def test_ingest_fmp_data_rejects_missing_configuration(
    monkeypatch,
    symbols,
    api_key,
    message,
):
    monkeypatch.setattr(
        fmp_ingestion,
        "get_settings",
        lambda: SimpleNamespace(
            fmp_symbols=symbols,
            fmp_api_key=api_key,
            fmp_api_base_url="https://example.test/stable/",
            s3_bucket="test-bucket",
            raw_prefix="raw",
        ),
    )

    with pytest.raises(ValueError, match=message):
        fmp_ingestion.ingest_fmp_data()
