#!/usr/bin/env bash
# Khởi động autocommit ở nền, ghi log vào logs/autocommit.log
set -euo pipefail
mkdir -p logs
if pgrep -f autocommit_on_save.sh >/dev/null 2>&1; then
  echo "[INFO] autocommit đã chạy."; exit 0
fi
nohup bash scripts/autocommit_on_save.sh >> logs/autocommit.log 2>&1 &
PID=$!
echo $PID > logs/autocommit.pid
echo "[INFO] Đã start autocommit PID=$PID (log: logs/autocommit.log)"
