"""Local, read-only browser for StockDB DuckDB tables and their lineage."""
from __future__ import annotations
import os
import sys
from pathlib import Path
import duckdb
import pandas as pd
import streamlit as st
from stock_production.tables import TableNames

def _load_project_env():
    """Load only what the viewer needs; never require or display the API key."""
    ...

def database_path() -> Path:
    ...

def build_lineage(tables: TableNames) -> dict[str, list[str]]:
    """Direct lineage from persistent DuckDB objects to tables/files/API sources."""
    ...

def classify_table(table_name: str) -> str:
    ...

def load_catalog(connection) -> tuple[pd.DataFrame, pd.DataFrame]:
    ...

def render_lineage(selected: str, upstream: list[str], downstream: list[str]):
    """Render a compact, dependency-free three-column relationship diagram."""
    ...

def main():
    ...
if __name__ == '__main__':
    main()
