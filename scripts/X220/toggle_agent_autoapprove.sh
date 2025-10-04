#!/usr/bin/env bash
# Script: toggle_agent_autoapprove.sh
# Mục tiêu: Bật / tắt chế độ auto approve cho agent chat.
# Cơ chế: sửa file marker agent_autoapprove.enabled dạng JSON.

set -euo pipefail
MARKER="agent_autoapprove.enabled"

usage() {
  echo "Dùng: $0 on|off|status"; exit 1
}

[ $# -ge 1 ] || usage
cmd=$1
timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)

init_if_missing() {
  if [ ! -f "$MARKER" ]; then
    echo "{\n  \"autoApprove\": false,\n  \"updatedAt\": \"$timestamp\",\n  \"note\": \"Tự tạo marker mặc định\"\n}" > "$MARKER"
  fi
}

show_status() {
  if grep -q '"autoApprove": true' "$MARKER" 2>/dev/null; then
    echo "autoApprove=ON"
  else
    echo "autoApprove=OFF"
  fi
}

init_if_missing

case "$cmd" in
  on)
    cat > "$MARKER" <<EOF
{
  "autoApprove": true,
  "updatedAt": "$timestamp",
  "note": "Bật qua toggle script"
}
EOF
    echo "[INFO] Đã bật autoApprove.";
    ;;
  off)
    cat > "$MARKER" <<EOF
{
  "autoApprove": false,
  "updatedAt": "$timestamp",
  "note": "Tắt qua toggle script"
}
EOF
    echo "[INFO] Đã tắt autoApprove.";
    ;;
  status)
    show_status;
    ;;
  *) usage ;;
esac

exit 0
