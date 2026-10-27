"""Executable entry point for the daily stock update pipeline."""
from pathlib import Path
import sys
from stock_production.pipelines.stock_daily_update import StockDailyUpdate

def main():
    ...
if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
