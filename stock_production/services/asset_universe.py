"""Download, persist, and read filtered stock or ETF ticker universes."""

import csv
import re
from pathlib import Path


class AssetUniverseService:
    """Build ticker lists from Alpha Vantage LISTING_STATUS CSV data."""

    REQUIRED_COLUMNS = {"symbol", "assetType", "status"}
    US_COMMON_STOCK_EXCHANGES = {"NASDAQ", "NYSE", "AMEX", "NYSE MKT"}
    NON_COMMON_SECURITY_NAME = re.compile(
        r"\b(?:ETFS?|ETNS?|ETPS?|WARRANTS?|WTS?|RIGHTS?|UNITS?|"
        r"PREFERRED|PREFERENCE SHARES?|DEBENTURES?|NOTES?|BONDS?|FUNDS?|"
        r"TEST STOCK|SYMBOLOGY TEST|WHEN ISSUED|WHENISSUED|"
        r"AUTOCALLABLE|COVERED CALL|DAILY TARGET|LEVERAGED|INVERSE)\b",
        re.IGNORECASE,
    )
    NON_COMMON_SECURITY_SYMBOL = re.compile(r"^[A-Z0-9][A-Z0-9.-]*$")

    def __init__(self, client):
        self.client = client

    def save_listing(self, output_path, asset_type="Stock", status="active"):
        """Save matching source rows as CSV, then return symbols read from it."""
        text = self.client.get_text("LISTING_STATUS")
        reader = csv.DictReader(text.splitlines())
        if not reader.fieldnames or not self.REQUIRED_COLUMNS.issubset(reader.fieldnames):
            raise ValueError(
                "Alpha Vantage did not return the expected listing CSV. "
                f"Response starts with: {text[:200]}"
            )

        rows = [
            row for row in reader
            if row.get("symbol", "").strip()
            and row.get("assetType", "").strip().lower() == asset_type.lower()
            and row.get("status", "").strip().lower() == status.lower()
        ]
        if not rows:
            raise ValueError(
                f"No {asset_type} rows with status={status} were returned. "
                f"Response starts with: {text[:200]}"
            )

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as output:
            writer = csv.DictWriter(output, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        with path.open("r", newline="", encoding="utf-8") as saved_file:
            saved_reader = csv.DictReader(saved_file)
            return sorted({row["symbol"].strip() for row in saved_reader})

    def save_active_stocks(self, output_path):
        """Save active US-listed common-stock candidates and return their symbols.

        LISTING_STATUS can label ETFs and other instruments as ``Stock``. Keep
        only the primary US equity venues and exclude clearly identified funds,
        warrants, units, rights, debt instruments, and synthetic test symbols.
        """
        text = self.client.get_text("LISTING_STATUS")
        reader = csv.DictReader(text.splitlines())
        required = self.REQUIRED_COLUMNS | {"exchange", "name"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(
                "Alpha Vantage did not return the expected listing CSV. "
                f"Response starts with: {text[:200]}"
            )
        source_rows = list(reader)
        rows = self.filter_active_us_stock_rows(source_rows)
        if not rows:
            raise ValueError("No active US-listed common-stock candidates were returned.")
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as output:
            writer = csv.DictWriter(output, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(
            f"Active US-listed stock universe: retained {len(rows):,} of "
            f"{len(source_rows):,} rows; excluded {len(source_rows) - len(rows):,} "
            "ETFs/derivatives/non-US-primary-exchange or non-active listings."
        )
        return sorted({row["symbol"].strip() for row in rows})

    def fetch_active_us_stock_rows(self):
        """Fetch LISTING_STATUS and return active US common-stock candidate rows."""
        text = self.client.get_text("LISTING_STATUS")
        reader = csv.DictReader(text.splitlines())
        required = self.REQUIRED_COLUMNS | {"exchange", "name"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(
                "Alpha Vantage did not return the expected listing CSV. "
                f"Response starts with: {text[:200]}"
            )
        rows = self.filter_active_us_stock_rows(reader)
        if not rows:
            raise ValueError("No active US-listed common-stock candidates were returned.")
        return reader.fieldnames, rows

    @staticmethod
    def write_rows(output_path, fieldnames, rows):
        """Atomically replace a listing CSV with the supplied source rows."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = path.with_name(f".{path.name}.tmp")
        with temporary_path.open("w", newline="", encoding="utf-8") as output:
            writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        temporary_path.replace(path)
        return path

    @classmethod
    def read_symbols(cls, csv_path, column="symbol"):
        """Read a symbol column from a CSV, matching its header case-insensitively."""
        with Path(csv_path).open("r", newline="", encoding="utf-8-sig") as source:
            reader = csv.DictReader(source)
            field = next(
                (name for name in (reader.fieldnames or []) if name.strip().lower() == column.lower()),
                None,
            )
            if field is None:
                raise ValueError(f"CSV is missing column {column}: {csv_path}")
            return {
                (row.get(field) or "").strip().upper()
                for row in reader
                if (row.get(field) or "").strip()
            }

    @classmethod
    def filter_active_us_stock_rows(cls, rows):
        """Filter listing rows already downloaded, keeping their original fields."""
        filtered = []
        for row in rows:
            symbol = (row.get("symbol") or "").strip()
            name = (row.get("name") or "").strip()
            exchange = (row.get("exchange") or "").strip().upper()
            asset_type = (row.get("assetType") or "").strip().lower()
            status = (row.get("status") or "").strip().lower()
            if not symbol or not name:
                continue
            if not cls.NON_COMMON_SECURITY_SYMBOL.fullmatch(symbol.upper()):
                continue
            if asset_type != "stock" or status != "active":
                continue
            if exchange not in cls.US_COMMON_STOCK_EXCHANGES:
                continue
            if cls.NON_COMMON_SECURITY_NAME.search(name):
                continue
            filtered.append(row)
        return filtered
