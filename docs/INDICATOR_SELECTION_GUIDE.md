# HƯỚNG DẪN BỘ CÔNG CỤ GIAO DỊCH - PHIÊN BẢN "VOLUME FIRST"

**Cập nhật lần cuối:** Tháng 10, 2025  
**Triết lý:** "Không tìm kiếm chỉ báo hoàn hảo, chỉ có hệ thống hoàn hảo."

---

## 1. TRIẾT LÝ NỀN TẢNG: THOÁT KHỎI "HỐ THỎ CHỈ BÁO"

Tài liệu này định nghĩa **Hệ thống Giao dịch Chính thức và Duy nhất**. Mục tiêu của nó là chấm dứt việc tìm kiếm và thay đổi chỉ báo liên tục. Chúng ta không giao dịch bằng "công cụ", chúng ta giao dịch bằng một "hệ thống".

**Quy tắc Chống Sa lầy:**
> "Edge không nằm trong một chỉ báo 'hoàn hảo', mà nằm trong một **HỆ THỐNG** có kỷ luật. Đừng tìm kiếm công cụ mới, hãy làm chủ **quy trình làm việc** giữa các công cụ hiện có."

Hệ thống này được xây dựng dựa trên một quy trình làm việc bất biến: **STRUCTURE (WHERE) -> CONFIRMATION (WHEN)**.

---

## 2. HỆ THỐNG GIAO DỊCH CHÍNH THỨC

Hệ thống này bao gồm 2 công cụ chính và 1 công cụ phụ trợ. Mỗi công cụ có một vai trò duy nhất và không thể thay thế.

### CÔNG CỤ #1: NỀN TẢNG CẤU TRÚC (THE STRUCTURE ENGINE)
- **Chỉ báo được chỉ định:** `Pi-3.4-Professional.pine`
- **Vai trò:** Xác định "Sân Chơi" (The Playing Field).
- **Nhiệm vụ:** Cung cấp các vùng và mức giá khách quan dựa trên **Volume** (POC, VAH, VAL) và bối cảnh khung thời gian lớn (HTF Lines).
- **KHÔNG DÙNG ĐỂ:** Tìm tín hiệu vào lệnh trực tiếp.

### CÔNG CỤ #2: ĐỘNG CƠ XÁC NHẬN (THE CONFIRMATION ENGINE)
- **Chỉ báo được chỉ định:** `CVPZero.pine`
- **Vai trò:** Cung cấp "Tín hiệu Kích hoạt" (The Trigger).
- **Nhiệm vụ:** Xác nhận hoạt động của **Dòng tiền** (Phân kỳ, VSA) CHỈ KHI giá đã ở trong "Sân Chơi" do `Pi-3.4` xác định.
- **KHÔNG DÙNG ĐỂ:** Giao dịch mọi tín hiệu mà nó tạo ra một cách mù quáng.

### CÔNG CỤ #3 (TÙY CHỌN): TINH CHỈNH ĐIỂM VÀO LỆNH (THE ENTRY REFINER)
- **Chỉ báo được chỉ định:** `SMPA-ORG.pine`
- **Vai trò:** "Last-minute confirmation".
- **Nhiệm vụ:** Sau khi đã có cấu trúc (VP) và xác nhận (CVD), có thể dùng `SMPA` để tìm một khối Order Block nhỏ hoặc mẫu nến để tối ưu hóa điểm vào lệnh và R:R.
- **CẢNH BÁO:** Không được dùng làm công cụ xây dựng hệ thống chính.

---

## 3. QUY TRÌNH LÀM VIỆC CHUẨN (THE STANDARD WORKFLOW)

Đây là quy trình 5 bước bất biến cho mọi quyết định giao dịch.

**BƯỚC 1: PHÂN TÍCH BỐI CẢNH (KHUNG D, W)**
- **Công cụ:** `Pi-3.4`
- **Hành động:** Xác định xu hướng chính của thị trường. Giá đang nằm trên hay dưới POC của tuần/tháng? EMA 200 đang dốc lên hay xuống? Chỉ giao dịch thuận theo xu hướng chính này.

**BƯỚC 2: XÁC ĐỊNH "SÂN CHƠI" (KHUNG 4H, 1H)**
- **Công cụ:** `Pi-3.4`
- **Hành động:** Xác định các mức **POC, VAH, VAL** của khung thời gian giao dịch chính. Đây là các vùng giá trị, vùng kháng cự/hỗ trợ khách quan của bạn.

**BƯỚC 3: CHỜ ĐỢI GIÁ VÀO VÙNG SĂN BẮN**
- **Hành động:** Không làm gì cả. Kiên nhẫn chờ đợi giá tiếp cận các cạnh của "Sân Chơi" (VAH hoặc VAL). Đây là bài kiểm tra kỷ luật quan trọng nhất.

**BƯỚC 4: TÌM KIẾM SỰ HỘI TỤ (KHUNG 1H, 15M)**
- **Công cụ:** `CVPZero`
- **Hành động:** KHI và CHỈ KHI giá đang ở trong "Vùng Săn Bắn", hãy nhìn xuống `CVPZero` và tìm kiếm ít nhất **2 tín hiệu xác nhận**, ví dụ:
    - Phân kỳ CVD+Price (Bullish/Bearish Divergence).
    - Tín hiệu VSA mạnh (Spring, Upthrust, SC, BC).
    - Bảng Multi-TF CVD đồng thuận.

**BƯỚC 5: THỰC THI & QUẢN LÝ**
- **Công cụ:** `SMPA` (tùy chọn) hoặc nến.
- **Hành động:** Sau khi có đủ xác nhận, tìm điểm vào lệnh tối ưu. Đặt Stoploss ngay lập tức dựa trên cấu trúc của `Pi-3.4` (ví dụ: dưới VAL). Xác định các mục tiêu giá (TP) tại POC và VAH.

---

## 4. CÁC CÔNG CỤ ĐÃ LOẠI BỎ (DEPRECATED INDICATORS)

Để đảm bảo sự tập trung và tránh "hố thỏ", các chỉ báo sau được xem là đã lỗi thời và **KHÔNG ĐƯỢC SỬ DỤNG** trong hệ thống này:

- **`VPP5.pine`:** Đã được tích hợp và nâng cấp trong `Pi-3.4`.
- **`CVD-Pro.pine`:** Đã được thay thế bằng `CVPZero` (phiên bản tinh chỉnh hơn).
- **`Better-CVD-Final.pine`:** Phiên bản cũ, đã loại bỏ.
- **Các chỉ báo lagging truyền thống:** RSI, MACD, Stochastic, Bollinger Bands (trên giá)...

---

## 5. CHECKLIST GIAO DỊCH TỐI THƯỢNG

Sử dụng checklist này cho MỌI giao dịch. Cần ít nhất 5/6 điều kiện để xem xét vào lệnh.

**VÍ DỤ CHO MỘT LỆNH LONG:**

- **[ ] CẤU TRÚC (WHERE):** Giá đang ở tại hoặc dưới mức **VAL** của `Pi-3.4`?
- **[ ] BỐI CẢNH HTF:** Giá có đang nằm trên **POC của khung thời gian cao hơn** không (tránh mua ở vùng premium)?
- **[ ] XU HƯỚNG:** Mây EMA trên `Pi-3.4` có đang hỗ trợ cho xu hướng tăng không?
- **[ ] DÒNG TIỀN (CVD):** Đường CVD trên `CVPZero` có đang đi lên hoặc tạo đáy cao hơn không?
- **[ ] HÀNH VI (VSA):** Có tín hiệu VSA hỗ trợ (ví dụ: Spring, SC, NS) tại vùng VAL không?
- **[ ] HỘI TỤ (CONFLUENCE):** Có tín hiệu Phân kỳ tăng (Bullish Divergence) xuất hiện cùng lúc không?

**Chỉ khi trả lời "CÓ" cho phần lớn các câu hỏi trên, đó mới là một "beautiful and sure setup".**