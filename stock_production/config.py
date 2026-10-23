"""Central configuration for stock and ETF production jobs."""

from dataclasses import dataclass
import os
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = PACKAGE_DIR.parent


def _load_local_env(path=PACKAGE_DIR / ".env"):
    """Load simple KEY=VALUE entries without requiring python-dotenv."""
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


@dataclass(frozen=True)
class AppConfig:
    """Immutable paths and runtime settings shared by production pipelines."""

    project_dir: Path
    data_dir: Path
    database_path: Path
    api_key: str
    api_base_url: str = "https://www.alphavantage.co/query"
    requests_per_minute: int = 70
    request_timeout_seconds: int = 60

    @classmethod
    def from_environment(cls):
        """Build settings from environment variables and stock_production/.env."""
        _load_local_env()
        project_dir = Path(os.environ.get("STOCKDB_PROJECT_DIR", PROJECT_DIR)).expanduser()
        data_dir = Path(
            os.environ.get("STOCKDB_DATA_DIR", project_dir / "data_acquisition")
        ).expanduser()
        database_path = Path(
            os.environ.get(
                "STOCKDB_DATABASE_PATH",
                project_dir / "database" / "stocks_screening.db",
            )
        ).expanduser()
        api_key = os.environ.get("ALPHAVANTAGE_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError(
                "Alpha Vantage API key is missing. Set ALPHAVANTAGE_API_KEY "
                "or add it to stock_production/.env."
            )
        rpm = int(os.environ.get("ALPHAVANTAGE_REQUESTS_PER_MINUTE", "70"))
        return cls(
            project_dir=project_dir,
            data_dir=data_dir,
            database_path=database_path,
            api_key=api_key,
            requests_per_minute=rpm,
        )

    @property
    def stock_list_path(self):
        return self.data_dir / "stock_list.csv"

    @property
    def daily_trading_dir(self):
        return self.data_dir / "daily_trading"

    @property
    def intraday_trading_dir(self):
        return self.data_dir / "intraday_trading"

    @property
    def daily_csv_path(self):
        return self.data_dir / "ALL_STOCKS_DAILY.csv"

    @property
    def etf_trading_daily_path(self):
        return self.data_dir / "etf_trading_daily.csv"

    @property
    def intraday_csv_path(self):
        return self.data_dir / "ALL_STOCKS_INTRADAY.csv"

    @property
    def overview_dir(self):
        return self.data_dir / "stocks_overview"

    @property
    def dividends_dir(self):
        return self.data_dir / "stocks_dividends"

    @property
    def earnings_dir(self):
        return self.data_dir / "stocks_earnings_calendar"

    @property
    def overview_csv_path(self):
        return self.data_dir / "stocks_overview.csv"

    @property
    def dividends_csv_path(self):
        return self.data_dir / "stocks_dividends.csv"

    @property
    def earnings_calendar_csv_path(self):
        return self.data_dir / "stocks_earnings_calendar.csv"
