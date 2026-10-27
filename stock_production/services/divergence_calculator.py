"""Pivot detection and regular (classic) divergence detection.

The approach follows the widely used "divergence for many indicators" logic:

1. Find pivot highs / lows on the closing price (a bar whose close is the
   highest / lowest within ``pivot_period`` bars on each side).
2. For each recent bar, look back at up to ``max_pivots`` pivots. A *negative*
   (bearish) regular divergence exists when price makes a higher high while the
   indicator makes a lower high; a *positive* (bullish) one is the mirror case.
3. The straight lines joining the pivot and the current bar, on both price and
   the indicator, must not be crossed by any bar in between.

All window sizes are constructor parameters. The defaults are the common public
defaults for this kind of indicator, not tuned values.
"""
import numpy as np
import pandas as pd
DEFAULT_INDICATORS = ('rsi', 'macd_hist', 'stk', 'moment', 'cci', 'vwmacd', 'cmf', 'mfi', 'obv')

class DivergenceCalculator:
    """Calculate pivot points and map regular divergence signals."""

    def __init__(self, pivot_period=5, max_pivots=10, max_lookback_bars=100, min_bars_between=5, max_pivot_history=20, indicators=DEFAULT_INDICATORS):
        ...

    def calculate_pivot_points(self, df, prd=None, max_array_size=None):
        """Return positions and closing values of recent pivot highs and lows.

Args:
    df: frame with an ``adjusted_close`` column, in time order.
    prd: bars on each side of the pivot (defaults to ``pivot_period``).
    max_array_size: keep at most this many recent pivots of each kind."""
        ...

    def _regular_divergence(self, df, positions, pivot_vals, src_list, src_pivot_list, bullish):
        """Shared scan for positive (bullish=True) or negative regular divergence."""
        ...

    def negative_regular_divergence(self, df, ph_positions, ph_vals, src_list, src_ph_list):
        ...

    def positive_regular_divergence(self, df, pl_positions, pl_vals, src_list, src_pl_list):
        ...

    def detect_all_divergences(self, df, ph_positions, ph_vals, pl_positions, pl_vals):
        """Run both scans for every configured indicator.

Returns ``{divergence_type: {bar_index: {"piv_idx": set, "name": set}}}``."""
        ...

    def calculate_full_analysis(self, df):
        """Per-ticker entry point: pivots -> divergences -> signal columns."""
        ...
