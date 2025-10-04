# Bộ sưu tập Pine Scripts (X220)

Thư mục này chứa các indicator Pine Script được migrate từ repo trước **TradingView-code** và đã được chuẩn hoá hậu tố `_X220` để phân biệt nguồn gốc / thế hệ.

## Mục tiêu
- Tập trung tất cả indicator vào một repo duy nhất.
- Tránh phân mảnh nhiều repository nhỏ.
- Dễ bảo trì, version hóa, review.

## Cấu trúc
- `*.pine`: Mỗi file là một indicator độc lập.
- Hậu tố `_X220`: Batch import từ máy ThinkPad X220 (phiên gốc).
- `scripts/X220/`: Các script tiện ích liên quan quy trình làm việc (tự động commit, export, ssh, logging terminal...).

## Script tiện ích kèm theo
| Script | Chức năng |
|--------|-----------|
| autocommit_on_save.sh | Tự commit khi save file |
| start_autocommit_bg.sh | Chạy autocommit nền |
| export_pines.sh | Gom Pine Scripts vào một thư mục |
| capture_external_terminal.sh | Ghi log phiên terminal ngoài |
| toggle_agent_autoapprove.sh | Bật/tắt auto approve agent |
| setup_github_ssh.sh | Thiết lập SSH cho GitHub |

## Quy ước đặt tên
- Khoảng trắng đổi thành `_`.
- Giữ dấu `+` để không mất meaning (CVD+Volume).
- Nếu cần chuẩn hoá thêm (ví dụ đổi `+` -> `_plus`) có thể thực hiện sau.

## Gợi ý phát triển tiếp
- Thêm header metadata thống nhất (version, author, source link).
- Viết script lint Pine (kết hợp API của TradingView nếu có quyền).
- Thêm test logic căn bản (nếu trích xuất thành mô-đun backtest).

## Liên hệ
Nếu bạn (tương lai) cần truy xuất lại repo gốc: nó đã được hợp nhất vào đây — hạn chế phục hồi nếu đã xoá.

