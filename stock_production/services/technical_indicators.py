"""Reusable technical indicator calculations for daily market data."""
import numpy as np
import pandas as pd
import numba

def _njit_without_cache(*args, **kwargs):
    ...

class TechnicalIndicatorCalculator:
    """Calculate the technical indicators used by stock and ETF pipelines."""

    def calculate_intraday_indicators(self, df):
        """Add VWMA20 to an intraday frame with close and volume columns."""
        ...

    def calculate_indicators_for_ticker(self, df):
        """Calculate the standard indicator set for one ticker's OHLCV frame."""
        ...
