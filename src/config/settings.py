import os


class Settings:
    def __init__(self):
        self.project_name = "FinLakehouse"
        self.finance_api_base_url = os.getenv(
            "FINANCE_API_BASE_URL",
            "https://example-finance-api.local",
        )
        self.finance_api_key = os.getenv("FINANCE_API_KEY", "")
        self.s3_bucket = os.getenv("S3_BUCKET", "finlakehouse-raw")
        self.raw_prefix = os.getenv("RAW_PREFIX", "raw")
        self.bronze_prefix = os.getenv("BRONZE_PREFIX", "bronze")
        self.silver_prefix = os.getenv("SILVER_PREFIX", "silver")
        self.gold_schema = os.getenv("GOLD_SCHEMA", "gold")
        self.output_path = os.getenv("OUTPUT_PATH", "data")


def get_settings():
    return Settings()
