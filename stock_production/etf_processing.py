"""Build ETF view, screened overview, and sector-to-stock mapping tables."""
from pathlib import Path
import sys
import duckdb
from stock_production.etf_preview_update import ETFPreviewUpdate

class ETFProcessing(ETFPreviewUpdate):
    """Refresh ETF preview data and derive the ETF SQL tables."""

    def _replace_sql_table(self, table_name, select_sql):
        """Create a staging table and atomically replace its destination."""
        ...

    def create_etf_view(self):
        """Join ETF theme rows to the requested profile fields, excluding sectors."""
        ...

    def create_etf_overview(self):
        """Keep the three largest non-leveraged ETFs in each theme subgroup."""
        ...

    def create_sector_stock_mapping(self):
        """Map only selected ETFs to nonzero sector and stock weights."""
        ...

    def run(self):
        """Refresh source data, then materialize the ETF view and mapping tables."""
        ...

def main():
    ...
if __name__ == '__main__':
    raise SystemExit(main())
