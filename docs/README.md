# Hướng dẫn sử dụng workspace Pine Script

- Đây là workspace đã được cấu trúc lại để tối ưu cho việc phát triển, quản lý version, backup, nâng cấp code PineScript.
- Đọc file WORKSPACE_STRUCTURE.md để hiểu rõ ý nghĩa từng thư mục và quy tắc quản lý code.
- Khi thêm code mới, hãy đặt đúng thư mục và đặt tên file rõ ràng.
- Khi cần quay lại phiên bản cũ, chỉ cần lấy file từ thư mục legacy hoặc improvements, hoặc dùng git checkout/tag.

## Các thư mục chính

- indicators/: Indicator chính, bản release
- strategies/: Chiến lược/backtest
- libraries/: Hàm dùng chung
- tests/: Unit test, backtest
- examples/: Demo, ví dụ
- docs/: Tài liệu, changelog, quy tắc
- legacy/: Bản gốc, backup, so sánh
- improvements/: Bản cải tiến, patch, thử nghiệm

---
Mọi thay đổi lớn nên ghi chú lại trong docs hoặc commit message.
