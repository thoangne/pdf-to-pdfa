# 📄 PDF to PDF/A Converter (Ghostscript)

## Giới thiệu
**PDF to PDF/A Converter** là công cụ chuyển đổi hàng loạt file **PDF** sang chuẩn **PDF/A** (định dạng lưu trữ lâu dài), sử dụng **Ghostscript** và giao diện **Tkinter**.  
Công cụ hỗ trợ chạy đa luồng (`ThreadPoolExecutor`) giúp tăng tốc xử lý, và tự động tìm đường dẫn Ghostscript trên máy.

---

## ✨ Tính năng
- 🖱 **Giao diện trực quan** (Tkinter GUI) – dễ sử dụng.
- 📂 **Chuyển đổi hàng loạt** PDF sang PDF/A.
- ⚡ **Xử lý đa luồng** giúp tăng tốc độ chuyển đổi.
- 🔍 **Tự động tìm Ghostscript** trong máy.
- 📝 **Xuất log lỗi** (`error_log.txt`) khi có file bị lỗi.
- 🚫 Không hiển thị cửa sổ CMD khi chạy chuyển đổi.

---

## 📦 Yêu cầu hệ thống
- **Python** ≥ 3.8
- **Ghostscript** (tải tại: [https://ghostscript.com/download](https://ghostscript.com/download))
- Thư viện Python:
  ```bash
  pip install tkinter
