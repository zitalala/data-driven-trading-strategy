"""Reusable Alpha Vantage HTTP client."""

import requests
import threading
import time


class AlphaVantageClient:
    """Small API client shared by stock and ETF data services."""

    def __init__(self, api_key, base_url, timeout=60, session=None,
                 requests_per_minute=70):
        if not api_key:
            raise ValueError("api_key must be provided")
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.session = session or requests.Session()
        self.min_request_interval = 60 / requests_per_minute
        self._last_request_started = None
        self._rate_limit_lock = threading.Lock()

    def _wait_for_request_slot(self):
        """Space request start times evenly without adding latency twice."""
        with self._rate_limit_lock:
            now = time.monotonic()
            if self._last_request_started is not None:
                wait_seconds = (
                    self.min_request_interval - (now - self._last_request_started)
                )
                if wait_seconds > 0:
                    time.sleep(wait_seconds)
            self._last_request_started = time.monotonic()

    def get_response(self, function, **params):
        """Request an Alpha Vantage endpoint and return its HTTP response."""
        self._wait_for_request_slot()
        query = {"function": function, "apikey": self.api_key, **params}
        response = self.session.get(
            self.base_url, params=query, timeout=self.timeout
        )
        response.raise_for_status()
        return response

    def get_json(self, function, **params):
        """Request and decode a JSON endpoint response."""
        return self.get_response(function, **params).json()

    def get_text(self, function, **params):
        """Request an endpoint whose response is text or CSV."""
        return self.get_response(function, **params).content.decode("utf-8")

    def close(self):
        self.session.close()
