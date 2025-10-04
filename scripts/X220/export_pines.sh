#!/usr/bin/env bash
# Script: export_pines.sh
# Mục tiêu: Gom tất cả file *.pine (kể cả trong reference/, src/) vào thư mục đích chỉ định
# Cách dùng:
#   bash scripts/export_pines.sh /đường/dẫn/đích indicators/X220
# Nếu không truyền tham số sẽ tạo thư mục ./_export_pines

set -euo pipefail
DEST="${1:-_export_pines}"
mkdir -p "$DEST"

echo "[INFO] Thu thập file .pine vào: $DEST"

# Duyệt tất cả file *.pine
mapfile -t FILES < <(find . -type f -name '*.pine' | sort)

if [ ${#FILES[@]} -eq 0 ]; then
  echo "[WARN] Không tìm thấy file .pine nào"; exit 0
fi

for f in "${FILES[@]}"; do
  base=$(basename "$f")
  # Chuẩn hóa tên: thay khoảng trắng bằng _ để tránh lỗi khi clone sang repo khác
  safe=${base// /_}
  cp "$f" "$DEST/$safe"
  echo "[COPY] $f -> $DEST/$safe"
done

echo "[DONE] Tổng cộng ${#FILES[@]} file."
echo "[GỢI Ý] Bạn có thể chép thư mục này vào repo Trading tại indicators/X220"
