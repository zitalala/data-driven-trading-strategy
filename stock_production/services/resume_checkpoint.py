"""Small durable checkpoint helpers for resumable aggregate CSV jobs."""

import csv
import hashlib
import json
import os
import tempfile
from pathlib import Path


def symbols_fingerprint(symbols):
    """Return a stable digest for an ordered symbol universe."""
    payload = "\n".join(sorted({str(symbol).strip() for symbol in symbols if symbol}))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def read_checkpoint(path):
    """Read checkpoint JSON, returning None when absent or invalid."""
    try:
        with Path(path).open("r", encoding="utf-8") as checkpoint_file:
            value = json.load(checkpoint_file)
        return value if isinstance(value, dict) else None
    except (OSError, ValueError):
        return None


def write_checkpoint(path, state):
    """Atomically replace a JSON checkpoint to survive abrupt interruption."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", prefix=f".{path.name}_", suffix=".tmp",
            dir=path.parent, encoding="utf-8", delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
            json.dump(state, temp_file, ensure_ascii=False, indent=2)
            temp_file.flush()
            os.fsync(temp_file.fileno())
        os.replace(temp_path, path)
    finally:
        if temp_path:
            temp_path.unlink(missing_ok=True)


def reconcile_partial_csv(path, fieldnames, completed_symbols, symbol_fields):
    """Drop rows from symbols not checkpointed, including a torn final write."""
    path = Path(path)
    completed_symbols = {str(symbol).strip().upper() for symbol in completed_symbols}
    if not path.exists():
        return

    temp_path = None
    try:
        with path.open("r", newline="", encoding="utf-8-sig") as source:
            reader = csv.DictReader(source)
            with tempfile.NamedTemporaryFile(
                mode="w", prefix=f".{path.name}_", suffix=".tmp",
                dir=path.parent, newline="", encoding="utf-8", delete=False,
            ) as temp_file:
                temp_path = Path(temp_file.name)
                writer = csv.DictWriter(
                    temp_file, fieldnames=fieldnames, extrasaction="ignore",
                    lineterminator="\n",
                )
                writer.writeheader()
                if reader.fieldnames:
                    symbol_field = next(
                        (name for name in symbol_fields if name in reader.fieldnames),
                        None,
                    )
                    if symbol_field:
                        for row in reader:
                            symbol = (row.get(symbol_field) or "").strip()
                            if symbol.upper() in completed_symbols:
                                writer.writerow(row)
                temp_file.flush()
                os.fsync(temp_file.fileno())
        os.replace(temp_path, path)
    finally:
        if temp_path:
            temp_path.unlink(missing_ok=True)
