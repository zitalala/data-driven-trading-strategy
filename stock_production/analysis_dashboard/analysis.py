"""Example analysis layer: theme-level breadth from the warehouse snapshot.

This is a deliberately simple, textbook example of the analysis layer that sits
on top of the warehouse. It shows the pattern (read upstream tables, compute a
result table in one transaction, let the dashboard read it) without any of the
author's proprietary signals, scores or screening rules, which are not part of
this repository.

Output table ``example_theme_summary`` has one row per ETF theme:

- ``n_stocks``: distinct constituent stocks with a snapshot row
- ``avg_return_1w`` / ``median_return_1w``: equal-weighted latest weekly return
- ``pct_above_vwma20``: share of members whose daily close is above their
  20-day volume-weighted moving average (a standard breadth measure)
- ``avg_rsi_1w``: average weekly RSI(14)
"""
from __future__ import annotations
import sys
from pathlib import Path
import duckdb
from stock_production.config import AppConfig
from stock_production.tables import TableNames

def build_theme_summary_sql(tables: TableNames) -> str:
    ...

def refresh(config: AppConfig | None=None, tables: TableNames | None=None) -> int:
    ...

def main() -> int:
    ...
if __name__ == '__main__':
    raise SystemExit(main())
