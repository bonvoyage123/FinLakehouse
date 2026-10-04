import requests


class FinancialDataClient:
    """Simple client wrapper for a market-data API."""

    def __init__(self, base_url, api_key=None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or ""
        self.session = requests.Session()

    def _request(self, endpoint, query_params=None):
        request_params = {"apikey": self.api_key}
        if query_params:
            request_params.update(query_params)

        url = self.base_url + "/" + endpoint
        response = self.session.get(url, params=request_params, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_daily_prices(self, ticker, start_date=None, end_date=None):
        query_params = {"ticker": ticker}
        if start_date:
            query_params["start_date"] = start_date
        if end_date:
            query_params["end_date"] = end_date
        return self._request("daily-prices", query_params)

    def get_company_profile(self, ticker):
        return self._request("company-profile", {"ticker": ticker})
