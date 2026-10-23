#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
APP_DIR="$PROJECT_ROOT/database_viewer"
VENV_DIR="$APP_DIR/.venv"
PYTHON="$VENV_DIR/bin/python"
REQUIREMENTS="$APP_DIR/requirements.txt"
INSTALL_STAMP="$VENV_DIR/.requirements-installed"

if [[ ! -f "$APP_DIR/app.py" || ! -f "$REQUIREMENTS" ]]; then
  print -u2 "Table explorer files not found: $APP_DIR"
  exit 1
fi

if [[ ! -x "$PYTHON" ]]; then
  print "First run: creating a virtual environment for the table explorer..."
  python3 -m venv "$VENV_DIR"
fi

if [[ ! -f "$INSTALL_STAMP" || "$REQUIREMENTS" -nt "$INSTALL_STAMP" ]]; then
  print "Installing or updating dependencies..."
  "$PYTHON" -m pip install -r "$REQUIREMENTS"
  touch "$INSTALL_STAMP"
fi

cd "$APP_DIR"
print "Starting the StockDB table explorer; press Control-C here to stop."
exec "$PYTHON" -m streamlit run app.py
