"""Choose which FMP data to fetch and where to save each response in S3."""

from datetime import datetime, timezone

from src.config.settings import get_settings
from src.ingestion.api_client import FinancialDataClient
from src.ingestion.s3_uploader import S3Uploader


def save_dataset(uploader, dataset_name, symbol, data, ingestion_date, run_id):
    object_key = (
        f"{dataset_name}/ingestion_date={ingestion_date}/"
        f"run_id={run_id}/{symbol}.json"
    )
    return uploader.upload_json(data, object_key)


def ingest_fmp_data(symbols=None):
    """Fetch configured FMP datasets and save their responses to S3."""
    settings = get_settings()
    if symbols is None:
        symbols = settings.fmp_symbols

    clean_symbols = []
    for symbol in symbols:
        symbol = symbol.strip()
        symbol = symbol.upper()
        if symbol:
            clean_symbols.append(symbol)

    if not clean_symbols:
        raise ValueError(
            "No FMP symbols configured. Set FMP_SYMBOLS or pass symbols."
        )
    if not settings.fmp_api_key:
        raise ValueError("FMP_API_KEY is required for FMP ingestion.")
    if not settings.s3_bucket:
        raise ValueError("S3_BUCKET is required for FMP ingestion.")

    client = FinancialDataClient(
        settings.fmp_api_base_url,
        settings.fmp_api_key,
    )
    uploader = S3Uploader(settings.s3_bucket, settings.raw_prefix)
    run_time = datetime.now(timezone.utc)
    run_date = run_time.date()
    ingestion_date = run_date.isoformat()
    run_id = run_time.strftime("%Y%m%dT%H%M%S%fZ")
    uploaded_keys = []

    for symbol in clean_symbols:
        prices = client.get_daily_prices(symbol)
        uploaded_keys.append(
            save_dataset(
                uploader,
                "daily_prices",
                symbol,
                prices,
                ingestion_date,
                run_id,
            )
        )

        profile = client.get_company_profile(symbol)
        uploaded_keys.append(
            save_dataset(
                uploader,
                "company_profiles",
                symbol,
                profile,
                ingestion_date,
                run_id,
            )
        )

        income_statement = client.get_income_statement(symbol)
        uploaded_keys.append(
            save_dataset(
                uploader,
                "income_statements",
                symbol,
                income_statement,
                ingestion_date,
                run_id,
            )
        )

        balance_sheet = client.get_balance_sheet(symbol)
        uploaded_keys.append(
            save_dataset(
                uploader,
                "balance_sheets",
                symbol,
                balance_sheet,
                ingestion_date,
                run_id,
            )
        )

        cash_flow = client.get_cash_flow_statement(symbol)
        uploaded_keys.append(
            save_dataset(
                uploader,
                "cash_flow_statements",
                symbol,
                cash_flow,
                ingestion_date,
                run_id,
            )
        )

    return uploaded_keys
