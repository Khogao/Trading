# Checklist Kiểm Thử Nhanh - CVPZero.pine (Refactored)

## ✅ Bước 1: Compile trên TradingView

1. Mở TradingView Pine Editor
2. Copy toàn bộ code từ `CVPZero.pine`
3. Paste vào Pine Editor
4. Click "Save" → Không có lỗi compile
5. Click "Add to Chart"

**Kết quả mong đợi**: Indicator load thành công, không có lỗi.

---

## ✅ Bước 2: Test Visual (3 charts)

### Chart 1: BTC/USDT 15m

- CVD divergence lines hiển thị: ✅ / ❌
- VSA labels (chỉ 10 loại): ✅ / ❌
- Volume colors (Z-score): ✅ / ❌
- Multi-TF table: ✅ / ❌

### Chart 2: ETH/USDT 1H

- CVD divergence lines hiển thị: ✅ / ❌
- VSA labels (chỉ 10 loại): ✅ / ❌
- Volume colors (Z-score): ✅ / ❌
- Multi-TF table: ✅ / ❌

### Chart 3: BTC/USDT 1D

- CVD divergence lines hiển thị: ✅ / ❌
- VSA labels (chỉ 10 loại): ✅ / ❌
- Volume colors (Z-score): ✅ / ❌
- Multi-TF table: ✅ / ❌

---

## ✅ Bước 3: Test Inputs (tùy chỉnh)

### Test Color Inputs

1. Mở Settings → "Màu sắc"
2. Đổi "Màu tăng (Bullish)" → Màu xanh dương
3. Đổi "Màu giảm (Bearish)" → Màu cam
4. Apply → Divergence lines đổi màu: ✅ / ❌

### Test Z-Score Thresholds

1. Mở Settings → "Volume Z-Score"
2. Đổi "Ngưỡng Z Rất cao" từ 2.5 → 3.0
3. Apply → Volume colors thay đổi: ✅ / ❌

### Test Alpha Controls

1. Mở Settings → "Hiển thị & Bảng"
2. Đổi "Độ trong suốt CVD Chart" từ 20 → 60
3. Apply → CVD plot mờ hơn: ✅ / ❌

### Test Zero-Line Offsets

1. Mở Settings → "Hiển thị & Bảng"
2. Đổi "Volume Zero Offset" từ 0 → 110000
3. Apply → Volume bars dịch lên baseline 110000: ✅ / ❌

---

## ✅ Bước 4: Test 10 VSA Signals

Kiểm tra VSA Legend table chỉ hiển thị 10 signals:

**Bearish (4)**:

1. SC - Selling Climax: ✅ / ❌
2. ND - No Demand: ✅ / ❌
3. UT - Upthrust: ✅ / ❌
4. WK - Weakness: ✅ / ❌

**Bullish (6)**:
5. BC - Buying Climax: ✅ / ❌
6. NS - No Supply: ✅ / ❌
7. SP - Spring: ✅ / ❌
8. SV - Stopping Volume: ✅ / ❌
9. ST - Strength: ✅ / ❌
10. SO - Shakeout: ✅ / ❌

**Các signals cũ không còn** (đã xóa):

- ❌ EF (Effort to Fall)
- ❌ ER (Effort to Rise)
- ❌ NE (No Effort Down)
- ❌ NU (No Effort Up)
- ❌ BH (Bag Holding)
- ❌ TE (Test)

---

## ✅ Bước 5: Test Alerts (nếu dùng)

1. Tạo alert mới → Chọn condition: "Regular Bullish CVD Divergence"
2. Save alert
3. Scroll lại 50-100 nến
4. Đếm số lần alert sẽ trigger
5. So sánh với version cũ (nếu có): Số lượng giống nhau ✅ / ❌

---

## ✅ Bước 6: Test Edge Cases

### Test với altcoin ít thanh khoản

- Symbol: DOGE/USDT 5m
- Indicator load thành công: ✅ / ❌
- Không crash: ✅ / ❌

### Test với offset cực lớn

- Volume Zero Offset = 1000000
- Chart vẫn render: ✅ / ❌

### Test với offset âm

- CVD Zero Offset = -50000
- Chart vẫn hoạt động: ✅ / ❌

---

## 📊 Kết quả Test

| Test | Kết quả | Ghi chú |
|------|---------|---------|
| Compile thành công | ✅ / ❌ | |
| Visual test (3 charts) | ✅ / ❌ | |
| Color inputs | ✅ / ❌ | |
| Z-Score thresholds | ✅ / ❌ | |
| Alpha controls | ✅ / ❌ | |
| Zero-line offsets | ✅ / ❌ | |
| 10 VSA signals | ✅ / ❌ | |
| Alerts | ✅ / ❌ | |
| Edge cases | ✅ / ❌ | |

**Tổng kết**: _____ / 9 tests passed

---

## 🐛 Báo lỗi (nếu có)

**Lỗi gặp phải**:

```
(Mô tả lỗi ở đây)
```

**Steps to reproduce**:

1. ...
2. ...
3. ...

**Screenshot** (nếu có):

- (Đính kèm ảnh)

---

## ✅ Hoàn thành

- [ ] Tất cả tests đã pass
- [ ] Không có lỗi compile
- [ ] Không có lỗi runtime
- [ ] Inputs hoạt động đúng
- [ ] 10 VSA signals hiển thị đúng
- [ ] Sẵn sàng để sử dụng production

**Ngày test**: _________  
**Người test**: _________  
**Kết quả**: ✅ PASS / ❌ FAIL
