"""Environment-configurable database table naming conventions."""

from dataclasses import dataclass
import os
import re


_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_PERIOD = re.compile(r"^[A-Za-z0-9]+$")


def _read_identifier(name, default):
    value = os.environ.get(name, default).strip()
    if not _IDENTIFIER.fullmatch(value):
        raise ValueError(f"{name} must be a simple SQL table identifier: {value!r}")
    return value


def _read_periods(name, default):
    values = tuple(value.strip() for value in os.environ.get(name, default).split(",") if value.strip())
    if not values or any(not _PERIOD.fullmatch(value) for value in values):
        raise ValueError(f"{name} must be a comma-separated list of valid suffixes")
    if len(values) != len(set(values)):
        raise ValueError(f"{name} contains duplicate suffixes")
    return values


@dataclass(frozen=True)
class TableNames:
    """Central table registry; stock and ETF daily names share periods."""

    stock_daily_prefix: str = "stock_metadata"
    etf_daily_prefix: str = "etf_metadata"
    daily_layer: str = "daily"
    daily_periods: tuple = ("1d", "1w", "1mo", "3mo", "6mo", "12mo")
    enriched_suffix: str = "with_divergences_and_indicators"
    intraday_prefix: str = "stock_metadata"
    intraday_layer: str = "intraday"
    intraday_periods: tuple = ("30min", "1h", "4h")
    stocks_overview: str = "stocks_overview"
    stocks_dividends: str = "stocks_dividends"
    stocks_earnings_calendar: str = "stocks_earnings_calendar"
    stocks_market: str = "stocks_market"
    stock_real_dividend_yield: str = "stock_real_dividend_yield"
    stock_daily_snapshot: str = "stock_daily_snapshot"
    stock_divergences_and_indicators_all: str = "stock_divergences_and_indicators_all"
    etf_market: str = "etf_market"
    etf_theme: str = "etf_theme"
    etf_preview: str = "etf_preview"
    etf_view: str = "etf_view"
    etf_overview: str = "etf_overview"
    etf_sector_stock_mapping: str = "etf_sector_stock_mapping"
    etf_trading_daily: str = "etf_trading_daily"
    etf_real_dividend_yield: str = "etf_real_dividend_yield"
    etf_daily_snapshot: str = "etf_daily_snapshot"
    etf_divergences_and_indicators_all: str = "etf_divergences_and_indicators_all"
    market_context_daily: str = "market_context_daily"
    market_context_indicators: str = "market_context_indicators"
    example_theme_summary: str = "example_theme_summary"

    @classmethod
    def from_environment(cls):
        """Load naming settings from environment variables or stock_production/.env."""
        from stock_production.config import _load_local_env

        _load_local_env()
        daily_periods = _read_periods("STOCKDB_DAILY_PERIODS", "1d,1w,1mo,3mo,6mo,12mo")
        intraday_periods = _read_periods("STOCKDB_INTRADAY_PERIODS", "30min,1h,4h")
        supported_daily = ("1d", "1w", "1mo", "3mo", "6mo", "12mo")
        if set(daily_periods) != set(supported_daily):
            raise ValueError("STOCKDB_DAILY_PERIODS currently supports exactly: " + ",".join(supported_daily))
        supported_intraday = {"30min", "1h", "4h"}
        if "30min" not in intraday_periods or not set(intraday_periods).issubset(supported_intraday):
            raise ValueError("STOCKDB_INTRADAY_PERIODS must include 30min and may include 1h and/or 4h")

        return cls(
            stock_daily_prefix=_read_identifier("STOCKDB_STOCK_DAILY_TABLE_PREFIX", "stock_metadata"),
            etf_daily_prefix=_read_identifier("STOCKDB_ETF_DAILY_TABLE_PREFIX", "etf_metadata"),
            daily_layer=_read_identifier("STOCKDB_DAILY_TABLE_LAYER", "daily"),
            daily_periods=daily_periods,
            enriched_suffix=_read_identifier("STOCKDB_ENRICHED_TABLE_SUFFIX", "with_divergences_and_indicators"),
            intraday_prefix=_read_identifier("STOCKDB_INTRADAY_TABLE_PREFIX", "stock_metadata"),
            intraday_layer=_read_identifier("STOCKDB_INTRADAY_TABLE_LAYER", "intraday"),
            intraday_periods=intraday_periods,
            stocks_overview=_read_identifier("STOCKDB_TABLE_OVERVIEW", "stocks_overview"),
            stocks_dividends=_read_identifier("STOCKDB_TABLE_DIVIDENDS", "stocks_dividends"),
            stocks_earnings_calendar=_read_identifier("STOCKDB_TABLE_EARNINGS_CALENDAR", "stocks_earnings_calendar"),
            stocks_market=_read_identifier("STOCKDB_TABLE_MARKET", "stocks_market"),
            stock_real_dividend_yield=_read_identifier("STOCKDB_STOCK_TABLE_REAL_DIVIDEND_YIELD", "stock_real_dividend_yield"),
            stock_daily_snapshot=_read_identifier("STOCKDB_STOCK_TABLE_DAILY_SNAPSHOT", "stock_daily_snapshot"),
            stock_divergences_and_indicators_all=_read_identifier("STOCKDB_STOCK_TABLE_DIVERGENCES_AND_INDICATORS_ALL", "stock_divergences_and_indicators_all"),
            etf_market=_read_identifier("STOCKDB_ETF_TABLE_MARKET", "etf_market"),
            etf_theme=_read_identifier("STOCKDB_ETF_TABLE_THEME", "etf_theme"),
            etf_preview=_read_identifier("STOCKDB_ETF_TABLE_PREVIEW", "etf_preview"),
            etf_view=_read_identifier("STOCKDB_ETF_TABLE_VIEW", "etf_view"),
            etf_overview=_read_identifier("STOCKDB_ETF_TABLE_OVERVIEW", "etf_overview"),
            etf_sector_stock_mapping=_read_identifier("STOCKDB_ETF_TABLE_SECTOR_STOCK_MAPPING", "etf_sector_stock_mapping"),
            etf_trading_daily=_read_identifier("STOCKDB_ETF_TABLE_TRADING_DAILY", "etf_trading_daily"),
            etf_real_dividend_yield=_read_identifier("STOCKDB_ETF_TABLE_REAL_DIVIDEND_YIELD", "etf_real_dividend_yield"),
            etf_daily_snapshot=_read_identifier("STOCKDB_ETF_TABLE_DAILY_SNAPSHOT", "etf_daily_snapshot"),
            etf_divergences_and_indicators_all=_read_identifier("STOCKDB_ETF_TABLE_DIVERGENCES_AND_INDICATORS_ALL", "etf_divergences_and_indicators_all"),
            market_context_daily=_read_identifier("STOCKDB_TABLE_MARKET_CONTEXT_DAILY", "market_context_daily"),
            market_context_indicators=_read_identifier("STOCKDB_TABLE_MARKET_CONTEXT_INDICATORS", "market_context_indicators"),
            example_theme_summary=_read_identifier("STOCKDB_TABLE_EXAMPLE_THEME_SUMMARY", "example_theme_summary"),
        )

    def _daily_table(self, prefix, period):
        if period not in self.daily_periods:
            raise ValueError(f"Unknown daily table period: {period}")
        return f"{prefix}_{period}_from_{self.daily_layer}"

    def stock_daily_base(self, period):
        return self._daily_table(self.stock_daily_prefix, period)

    def etf_daily_base(self, period):
        return self._daily_table(self.etf_daily_prefix, period)

    def stock_daily_enriched(self, period):
        return f"{self.stock_daily_base(period)}_{self.enriched_suffix}"

    def etf_daily_enriched(self, period):
        return f"{self.etf_daily_base(period)}_{self.enriched_suffix}"

    def intraday(self, period):
        if period not in self.intraday_periods:
            raise ValueError(f"Unknown intraday table period: {period}")
        return f"{self.intraday_prefix}_{period}_from_{self.intraday_layer}"

    @property
    def stock_daily_base_tables(self):
        return tuple(self.stock_daily_base(period) for period in self.daily_periods)

    @property
    def stock_daily_enriched_tables(self):
        return tuple(self.stock_daily_enriched(period) for period in self.daily_periods)

    @property
    def etf_daily_base_tables(self):
        return tuple(self.etf_daily_base(period) for period in self.daily_periods)

    @property
    def etf_daily_enriched_tables(self):
        return tuple(self.etf_daily_enriched(period) for period in self.daily_periods)

    @property
    def intraday_indicator_tables(self):
        return tuple(self.intraday(period) for period in self.intraday_periods if period != "30min")
