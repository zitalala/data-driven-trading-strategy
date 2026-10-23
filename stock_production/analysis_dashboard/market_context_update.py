"""Download non-ETF market context and calculate its RSI/divergence snapshots."""
from __future__ import annotations
import csv
import io
import os
import sys
import tempfile
from pathlib import Path
import duckdb
import pandas as pd
import requests
from stock_production.clients.alpha_vantage import AlphaVantageClient
from stock_production.config import AppConfig, _load_local_env
from stock_production.services.divergence_calculator import DivergenceCalculator
from stock_production.services.technical_indicators import TechnicalIndicatorCalculator
from stock_production.tables import TableNames
BREADTH_SYMBOLS = ('S5TH', 'S5FI')
CBOE_VIX_HISTORY_URL = 'https://cdn-api.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv'
FX_PAIR = ('AUD', 'USD')
TREASURY_MATURITY = '10year'
PERIODS = ('1d', '1w', '1mo', '3mo', '6mo', '12mo')
RAW_COLUMNS = ('ticker', 'date', 'open', 'high', 'low', 'close', 'value', 'source', 'source_status')

class MarketContextUpdate:
    """Refresh breadth, volatility, FX, and Treasury daily series for the dashboard."""

    def __init__(self, config=None, tables=None, api=None):
        ...

    def _get_json(self, label, function, **params):
        """Request JSON without allowing HTTP errors to echo the credential URL."""
        ...

    @staticmethod
    def _check_payload(payload, label):
        ...

    @staticmethod
    def _time_series_key(payload):
        ...

    @staticmethod
    def _ohlc_rows(ticker, source, series):
        ...

    def _download_index(self, symbol):
        ...

    def _derive_breadth_proxy_rows(self):
        """Compute S5TH/S5FI-like values from current VOO holdings and stock history."""
        ...

    def _download_vix_cboe(self):
        """Use Cboe's official, daily updated public VIX history CSV."""
        ...

    def _download_fx(self):
        ...

    def _download_treasury(self):
        ...

    def download_all(self):
        """Fetch sources independently; retain cached series when one API is unavailable."""
        ...

    @staticmethod
    def _period_end(day, period):
        ...

    def _period_bars(self, frame, period):
        ...

    def _calculate_latest_period(self, bars):
        ...

    def calculate_latest_indicators(self, raw_frame, statuses):
        ...

    def _replace_from_frame(self, table_name, frame):
        ...

    def run(self):
        ...

def main():
    ...
if __name__ == '__main__':
    raise SystemExit(main())
