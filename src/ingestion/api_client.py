"""Ask the FMP API for data and return the response."""

import requests


class FinancialDataClient:
    """Request prices, company profiles, and financial statements from FMP."""

    def __init__(self, base_url, api_key=None):
        self.base_url = base_url.rstrip("/")
        if api_key is None:
            self.api_key = ""
        else:
            self.api_key = api_key
        self.session = requests.Session()

    def _request(self, endpoint, query_params=None):
        request_params = {"apikey": self.api_key}
        if query_params is not None:
            for name, value in query_params.items():
                request_params[name] = value

        url = self.base_url + "/" + endpoint
        response = self.session.get(url, params=request_params, timeout=30)
        response.raise_for_status()
        response_data = response.json()
        return response_data

    def get_daily_prices(self, ticker, start_date=None, end_date=None):
        query_params = {"symbol": ticker}
        if start_date:
            query_params["from"] = start_date
        if end_date:
            query_params["to"] = end_date
        return self._request("historical-price-eod/full", query_params)

    def get_company_profile(self, ticker):
        query_params = {"symbol": ticker}
        return self._request("profile", query_params)

    def get_income_statement(self, symbol):
        query_params = {"symbol": symbol}
        return self._request("income-statement", query_params)

    def get_balance_sheet(self, symbol):
        query_params = {"symbol": symbol}
        return self._request("balance-sheet-statement", query_params)

    def get_cash_flow_statement(self, symbol):
        query_params = {"symbol": symbol}
        return self._request("cash-flow-statement", query_params)
