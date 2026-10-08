import os
from pathlib import Path

from dotenv import load_dotenv


class Settings:
    def __init__(self):
        env_file = Path(__file__).resolve().parents[2] / "config" / ".env"
        load_dotenv(dotenv_path=env_file, override=False)

        self.project_name = "FinLakehouse"
        self.fmp_api_base_url = os.getenv(
            "FMP_API_BASE_URL",
            "https://financialmodelingprep.com/stable/",
        )
        self.fmp_api_key = os.getenv("FMP_API_KEY", "")
        self.s3_bucket = os.getenv("S3_BUCKET", "finlakehouse-raw")
        self.raw_prefix = os.getenv("RAW_PREFIX", "raw")
        self.fmp_symbols = tuple(
            symbol.strip()
            for symbol in os.getenv("FMP_SYMBOLS", "").split(",")
            if symbol.strip()
        )
        self.bronze_prefix = os.getenv("BRONZE_PREFIX", "bronze")
        self.silver_prefix = os.getenv("SILVER_PREFIX", "silver")
        self.gold_schema = os.getenv("GOLD_SCHEMA", "gold")
        self.output_path = os.getenv("OUTPUT_PATH", "data")


def get_settings():
    return Settings()
