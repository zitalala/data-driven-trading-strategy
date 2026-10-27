#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
APP_DIR="$PROJECT_ROOT/stock_production/analysis_dashboard"
VENV_DIR="$APP_DIR/.venv"
PYTHON="$VENV_DIR/bin/python"
REQUIREMENTS="$APP_DIR/requirements.txt"
INSTALL_STAMP="$VENV_DIR/.requirements-installed"

if [[ ! -f "$APP_DIR/app.py" || ! -f "$REQUIREMENTS" ]]; then
  print -u2 "Dashboard files not found: $APP_DIR"
  exit 1
fi

if [[ ! -x "$PYTHON" ]]; then
  print "First run: creating a virtual environment for the dashboard..."
  python3 -m venv "$VENV_DIR"
fi

if [[ ! -f "$INSTALL_STAMP" || "$REQUIREMENTS" -nt "$INSTALL_STAMP" ]]; then
  print "Installing or updating dashboard dependencies..."
  "$PYTHON" -m pip install -r "$REQUIREMENTS"
  touch "$INSTALL_STAMP"
fi

cd "$APP_DIR"
print "Starting the StockDB dashboard; press Control-C here to stop."
exec "$PYTHON" -m streamlit run app.py
