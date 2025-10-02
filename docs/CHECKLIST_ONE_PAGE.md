# CHECKLIST MỘT TRANG — VP‑CVD + Greg Sanity Check

Mục tiêu: nhanh, rõ ràng, dán trước màn hình. Nếu không thỏa → KHÔNG VÀO LỆNH.

PRE‑TRADE (phải tick tất cả bắt buộc)
- [ ] Structure: Giá ở VAL (long) / VAH (short) hoặc gần POC cho TP
- [ ] HTF POC: HTF POC ủng hộ hướng vào lệnh (không buy premium / không sell discount)
- [ ] Order flow: CVD direction phù hợp (cvd rising → long; cvd falling → short)
- [ ] VSA: Có tín hiệu phù hợp (Spring/Stopping Vol → long; Upthrust/No Supply → short)
- [ ] Volume: Volume Z‑score ≥ threshold (ví dụ 1.0)
- [ ] MTF: Multi‑TF CVD aligned (15m, 1H, 4H) OR MTF filter disabled
- [ ] Stop loss đã đặt (theo ATR hoặc recent swing)
- [ ] Position size tính theo % rủi ro (riskPercent) và không vượt giới hạn vốn

GREG SANITY CHECK (bắt buộc 3 điều)
- [ ] Stop loss xác định và không thay đổi
- [ ] Lệnh KHÔNG phải để "gỡ" lỗ hoặc để trả thù thị trường
- [ ] Có tối thiểu 6/8 điều kiện PRE‑TRADE ở trên

IN‑TRADE (giữ nguyên kỷ luật)
- [ ] Stop vẫn còn và không di chuyển
- [ ] Không tăng kích thước khi lệnh thua
- [ ] Nếu trend/volume thay đổi xấu → đóng sớm hoặc giảm kích thước
- [ ] Time‑based rule: nếu không có movement trong X bars → close (ví dụ 16 bars trên 15m)

POST‑TRADE (sau đóng lệnh)
- [ ] Lưu screenshot setup (trước entry)
- [ ] Ghi nhanh cảm xúc & lý do vào trade journal
- [ ] Ghi compliance: đã tick bao nhiêu mục checklist?
- [ ] Tính P&L và cập nhật metrics (win rate, avg R:R)

QUICK ACTIONS (1 dòng mỗi mục)
- Nếu thiếu stop → KHÔNG VÀO
- Nếu trade để gỡ lỗ → PASS
- Nếu < 6 điều kiện → PASS
- Nếu 2 thua liên tiếp → nghỉ 1 giờ

HOW TO USE
1. Dán file này trên màn hình hoặc in ra.
2. Trước mỗi entry: tick từng mục.
3. Sau trade: cập nhật `TRADE_JOURNAL_TEMPLATE.md`.

---
*Phiên bản: 1.0 — Created Oct 2025*