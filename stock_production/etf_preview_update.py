"""Refresh the curated ETF universe and ETF_PROFILE preview data."""
import csv
import json
import os
import re
import sys
import tempfile
from pathlib import Path
import duckdb
from stock_production.clients.alpha_vantage import AlphaVantageClient
from stock_production.config import AppConfig
from stock_production.tables import TableNames

class ETFPreviewUpdate:
    """Refresh the curated ETF theme table and ETF_PROFILE preview table."""

    def __init__(self, config=None, tables=None, api=None):
        ...

    def load_theme_universe(self):
        """Replace the etf_theme table from the curated CSV after validation."""
        ...

    @staticmethod
    def _replace_table(connection, staging_table, table_name):
        """Atomically replace a DuckDB table with its validated staging table."""
        ...

    @staticmethod
    def _flatten_profile(value, prefix=''):
        """Flatten nested profile dictionaries; preserve arrays as JSON text."""
        ...

    @staticmethod
    def _api_error(payload):
        """Return quota/API-level errors without exposing request details."""
        ...

    def _iter_universe(self):
        """Yield the curated ETFs and add benchmarks from the full ETF listing."""
        ...

    def _benchmark_rows(self):
        """Read benchmark metadata from etf_list.csv, outside the theme universe."""
        ...

    def refresh_benchmark_profiles(self):
        """Download only benchmark profiles and merge them into preview CSV/table."""
        ...

    def download_profiles(self):
        """Fetch ETF_PROFILE per ticker and atomically write one wide CSV."""
        ...

    def load_preview_table(self):
        """Import etf_preview.csv and atomically replace the DuckDB preview table."""
        ...

    def run(self):
        """Refresh the ETF theme source and the relatively static ETF profile."""
        ...

def main():
    ...
if __name__ == '__main__':
    raise SystemExit(main())
