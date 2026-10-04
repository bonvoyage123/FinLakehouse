from src.config.settings import get_settings
from src.ingestion.api_client import FinancialDataClient


def main():
    settings = get_settings()
    client = FinancialDataClient(settings.finance_api_base_url, settings.finance_api_key)
    print(f"Project: {settings.project_name}")
    print(f"API base URL: {client.base_url}")


if __name__ == "__main__":
    main()
