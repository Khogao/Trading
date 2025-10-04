#!/usr/bin/env bash
# Script: capture_external_terminal.sh
# Mục đích: Ghi lại (record) toàn bộ phiên làm việc terminal BÊN NGOÀI VS Code
# và lưu log vào thư mục logs/ để bạn (và cửa sổ chat trong VS Code) có thể xem.
#
# CÁCH DÙNG (rất đơn giản):
# 1. Mở một terminal ngoài (ví dụ: Gnome Terminal)
# 2. cd /home/phi/Documents/TradingView-code
# 3. bash scripts/capture_external_terminal.sh
# 4. Sau đó dùng bình thường: gõ lệnh của bạn. Mọi thứ sẽ tự ghi vào file.
# 5. Kết thúc phiên bằng phím: Ctrl + D (hoặc gõ exit)
#
# File log sẽ có dạng: logs/external_session_YYYYmmdd_HHMMSS.log
# Bạn có thể mở/tail trong VS Code để chat agent đọc nội dung.
#
# Nếu muốn xem realtime trong VS Code:
#   1. Vào VS Code mở terminal tích hợp.
#   2. Chạy: tail -f logs/external_session_<tên_file>.log
#   3. Dừng tail bằng Ctrl + C
#
# YÊU CẦU: lệnh 'script' có sẵn trên đa số distro Linux (util-linux). Nếu thiếu: sudo apt install bsdutils (hoặc util-linux)

set -euo pipefail
mkdir -p logs
STAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="logs/external_session_${STAMP}.log"

echo "[INFO] Bắt đầu ghi phiên terminal vào: $LOG_FILE"
echo "[INFO] Thoát bằng Ctrl + D hoặc gõ 'exit' để dừng."

# -f để flush realtime, -q để giảm banner phụ.
script -q -f "$LOG_FILE"

echo "[INFO] Đã kết thúc. File log: $LOG_FILE"
echo "[GỢI Ý] Mở VS Code > Explorer > logs/ và click file để xem hoặc tail -f để theo dõi trực tiếp."
