#!/bin/zsh
set -euo pipefail

LABEL="com.stockdb.daily-market-update"
GUI_DOMAIN="gui/$(id -u)"
TARGET_PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

launchctl bootout "$GUI_DOMAIN/$LABEL" >/dev/null 2>&1 || true
launchctl disable "$GUI_DOMAIN/$LABEL" >/dev/null 2>&1 || true
rm -f "$TARGET_PLIST"
sudo pmset repeat cancel
echo "Removed the daily job and the repeating wake schedule. Existing logs are kept in logs/."
