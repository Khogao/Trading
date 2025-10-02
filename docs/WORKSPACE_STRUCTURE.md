# TradingView Pine Script Workspace Structure

## 📝 **PROJECT AUTHORSHIP**

**ALL CODE in this workspace:** Built 100% by us (Khogao + AI Assistant)

**Greg's Role:**
- ✅ Philosophy teacher (Manifesto, 5-year journey lessons)
- ✅ Inspiration for indicator naming (Greg_*, GHU_*, etc.)
- ❌ **Did NOT write any indicator code**

**Indicators named "Greg_*" = Honoring his philosophy, not his code.**

---

## Mục đích

Tài liệu này giúp bạn hiểu và quản lý workspace Pine Script một cách tối ưu cho việc phát triển, lưu trữ, version tracking, và nâng cấp code.

## Cấu trúc thư mục

```
/indicators/         # Indicator chính, bản release, code đang dùng
/strategies/         # Các chiến lược/backtest
/libraries/          # Hàm dùng chung, utils, function
/tests/              # Test, backtest, unit test
/examples/           # Demo, ví dụ, cấu hình mẫu
/docs/               # Tài liệu, hướng dẫn, changelog, quy tắc
/legacy/             # Bản gốc, bản so sánh, bản cũ, backup
/improvements/       # Các bản cải tiến, thử nghiệm, patch, fix
```

## Hướng dẫn sử dụng

- **indicators/**: Chỉ chứa các indicator đã hoàn thiện, đang sử dụng hoặc bản release.
- **strategies/**: Chứa các file chiến lược giao dịch, backtest.
- **libraries/**: Chứa các hàm dùng chung, file function, utils.
- **tests/**: Chứa các file kiểm thử, unit test, backtest configs.
- **examples/**: Chứa các ví dụ, cấu hình mẫu, demo.
- **docs/**: Chứa tài liệu hướng dẫn, changelog, quy tắc code, mô tả workspace.
- **legacy/**: Lưu trữ các bản gốc, bản cũ, bản backup, so sánh, file chưa chỉnh sửa.
- **improvements/**: Lưu các bản cải tiến, patch, thử nghiệm, bản fix lỗi, bản nâng cao.

## Quy tắc đặt tên file

- `indicator_name.v1.pine`, `indicator_name.v2.pine`, `indicator_name.backup.pine`, `indicator_name.experimental.pine`
- Ghi chú rõ version, trạng thái (org, fixed, test, backup, improved, ...)

## Quy trình quản lý version

- Sử dụng git branch cho các nhánh phát triển lớn (feature, hotfix, refactor)
- Tag các bản release ổn định
- Ghi chú thay đổi (changelog) trong `/docs/` hoặc commit message rõ ràng
- Khi cần quay lại version cũ, chỉ cần checkout branch/tag hoặc lấy file từ `/legacy/` hoặc `/improvements/`

## Lưu ý

- Luôn commit đầy đủ, ghi rõ nội dung thay đổi.
- Đặt tên file, thư mục rõ ràng, nhất quán.
- Đọc kỹ file này trước khi thêm/sửa/xóa code trong workspace.

---
Mọi thắc mắc hoặc góp ý, hãy bổ sung vào file này hoặc tạo issue trên Github repo.
