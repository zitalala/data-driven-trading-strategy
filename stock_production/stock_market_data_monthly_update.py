"""Refresh stock overview, dividend, and earnings data without per-ticker files."""
import csv
import io
import json
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
import duckdb
from stock_production.clients.alpha_vantage import AlphaVantageClient
from stock_production.config import AppConfig
from stock_production.schemas.overview import OVERVIEW_FIELDS
from stock_production.services.resume_checkpoint import read_checkpoint, reconcile_partial_csv, symbols_fingerprint, write_checkpoint
from stock_production.services.asset_universe import AssetUniverseService
from stock_production.tables import TableNames
DIVIDEND_FIELDS = ('symbol', 'ex_dividend_date', 'declaration_date', 'record_date', 'payment_date', 'amount')
EARNINGS_FIELDS = ('symbol', 'name', 'reportDate', 'fiscalDateEnding', 'estimate', 'currency', 'timeOfTheDay')

class StockMarketMonthlyUpdate:
    """Download and materialize stock market reference data as aggregate files."""

    def __init__(self, config=None):
        ...

    def _prepare_resume(self, tickers):
        """Start a new market-data checkpoint when the ticker universe changes."""
        ...

    @staticmethod
    def _copy_completed_rows(source_path, target_path, completed):
        """Seed a new partial CSV from completed rows in a prior published file."""
        ...

    def _save_resume(self):
        ...

    def cleanup_legacy_ticker_files(self):
        """Remove old per-ticker caches once; this workflow no longer recreates them."""
        ...

    def refresh_candidate_stock_list(self):
        """Fetch the full current active-stock candidate universe for Overview discovery."""
        ...

    def keep_overview_verified_stock_list(self, candidate_tickers):
        """Narrow stock_list.csv to active candidates with valid Overview responses."""
        ...

    @staticmethod
    def _has_api_error(payload):
        ...

    @staticmethod
    def _parse_overview(text, ticker):
        ...

    @staticmethod
    def _parse_dividends(text, ticker):
        ...

    @staticmethod
    def _parse_earnings(text, ticker):
        ...

    def _download_dataset(self, tickers, function, output_path, fields, parser, **params):
        """Resume a dataset from its last completed ticker and publish it atomically."""
        ...

    def _record_skipped_ticker(self, function, ticker, attempts, reason):
        """Append diagnostics for an unavailable ticker that exhausted retries."""
        ...

    def download_overview(self, tickers):
        ...

    def download_dividends(self, tickers):
        ...

    def download_earnings_calendar(self, tickers):
        ...

    @staticmethod
    def _replace_table_from_csv(connection, table_name, csv_path):
        """Import an aggregate CSV through staging before replacing its table."""
        ...

    def import_tables(self, connection):
        ...

    def create_market_table(self, connection):
        """Join the refreshed overview, dividend, and earnings tables."""
        ...

    def run(self):
        ...

def main():
    ...
if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
