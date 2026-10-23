#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-$(command -v python3)}"
LABEL="com.stockdb.daily-market-update"
SOURCE_PLIST="$PROJECT_ROOT/launchers/$LABEL.plist"
AGENT_DIR="$HOME/Library/LaunchAgents"
TARGET_PLIST="$AGENT_DIR/$LABEL.plist"
GUI_DOMAIN="gui/$(id -u)"

if [[ -z "$PYTHON_BIN" || ! -x "$PYTHON_BIN" ]]; then
  echo "python3 not found. Set PYTHON_BIN to the interpreter you want the schedule to use."
  exit 1
fi
if [[ ! -f "$PROJECT_ROOT/stock_production/.env" ]]; then
  echo "Missing $PROJECT_ROOT/stock_production/.env; the daily job reads the API key from it."
  exit 1
fi

mkdir -p "$PROJECT_ROOT/logs" "$AGENT_DIR"
chmod 700 "$PROJECT_ROOT/logs"
sed -e "s|{{PROJECT_ROOT}}|$PROJECT_ROOT|g" -e "s|{{PYTHON_BIN}}|$PYTHON_BIN|g" "$SOURCE_PLIST" > "$TARGET_PLIST"
chmod 644 "$TARGET_PLIST"

launchctl bootout "$GUI_DOMAIN/$LABEL" >/dev/null 2>&1 || true
launchctl bootstrap "$GUI_DOMAIN" "$TARGET_PLIST"
launchctl enable "$GUI_DOMAIN/$LABEL"

echo "Scheduling the Mac to wake Tue-Sat at 08:25 local time (after the US close)."
sudo pmset repeat wake TWRFS 08:25:00

echo "Daily refresh enabled: Tue-Sat at 08:30 local time."
echo "Log: $PROJECT_ROOT/logs/daily_market_update.log"
echo "Launch agent: $TARGET_PLIST"
pmset -g sched
