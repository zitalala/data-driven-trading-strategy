"""Run the complete daily stock and ETF market-data refresh in dependency order."""
from pathlib import Path
import argparse
import subprocess
import sys
from datetime import datetime
BASE_JOBS = (('Refresh and validate stock_list.csv (active listings with a verified Overview)', 'stock_production/stock_universe_update.py'), ('Stock daily prices, indicators and divergences', 'stock_production/stock_trading_data_daily_update.py'), ('Refresh the Alpha Vantage ETF listing (etf_list.csv)', 'stock_production/etf_list_download.py'), ('ETF profiles, screened ETF overview and sector-stock mapping', 'stock_production/etf_processing.py'), ('ETF daily prices, indicators and divergences', 'stock_production/etf_trading_daily_update.py'), ('Market context: breadth proxies, VIX, AUDUSD, US10Y', 'stock_production/analysis_dashboard/market_context_update.py'), ('Refresh example analysis tables for the dashboard', 'stock_production/analysis_dashboard/analysis.py'))
STOCK_MARKET_JOB = ('Stock overview / dividends / earnings / stocks_market', 'stock_production/stock_market_data_monthly_update.py')

def main(argv=None):
    ...
if __name__ == '__main__':
    raise SystemExit(main())
