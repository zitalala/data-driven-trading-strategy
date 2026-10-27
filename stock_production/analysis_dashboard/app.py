"""Example StockDB dashboard (read-only Streamlit app).

Pages:
1. Theme breadth: the example_theme_summary table produced by analysis.py.
2. Ticker explorer: daily price, VWMA20, RSI and detected divergences.
3. Market context: raw history for the macro / breadth series.

This public version intentionally contains no proprietary signals, scoring or
screening rules.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path
import altair as alt
import duckdb
import pandas as pd
import streamlit as st
from stock_production.tables import TableNames

def database_path() -> Path:
    ...

@st.cache_resource
def connect(path: str):
    ...

def table_exists(con, name: str) -> bool:
    ...

def query(con, sql: str, params=None) -> pd.DataFrame:
    ...
