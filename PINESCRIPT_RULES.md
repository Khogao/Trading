# CÁC NGUYÊN TẮC VÀNG CHO PINE SCRIPT V5

Đây là những quy tắc BẮT BUỘC phải tuân thủ khi viết hoặc sửa bất kỳ đoạn code Pine Script nào.

## 1. Luôn luôn sử dụng Pine Script phiên bản 5

Mọi script phải bắt đầu bằng `//@version=5`. Không bao giờ được dùng phiên bản cũ hơn.

## 2. Quy tắc xuống dòng để không bị lỗi

Để xuống dòng trong một lệnh gọi hàm có nhiều tham số, phải thụt vào đầu dòng (indent), KHÔNG được dùng dấu gạch chéo ngược (`\`).

- **ĐÚNG:**
  ```pinescript
  plot(
      series=close,
      title="My Plot"
      )
  ```

- **SAI:**
  ```pinescript
  plot(series=close,
  title="My Plot")
  ```

## 3. Quy tắc khai báo biến

Luôn sử dụng toán tử `:=` để gán lại giá trị cho một biến đã được khai báo. Chỉ dùng `=` khi khai báo lần đầu tiên.

- **ĐÚNG:**
  ```pinescript
  myVar = close
  if (bar_index > 10)
      myVar := high
  ```

## 4. Các hàm `input` và `plot`

Sử dụng các hàm input mới của v5 (ví dụ: `input.int()`, `input.float()`) và luôn đặt tên cho các tham số trong hàm `plot()` (ví dụ: `series=close`, `color=color.red`).
