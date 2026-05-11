# Thông tin Dự án: E-commerce Data Lakehouse (Batch Pipeline)

## 1. Tổng quan Dự án (Project Overview)
Dự án này là một hệ thống **Modern Batch Data Pipeline** được thiết kế để trích xuất dữ liệu giả lập từ sàn thương mại điện tử (E-commerce) và dữ liệu tỷ giá tiền tệ từ public API. Dữ liệu sau đó sẽ được nạp vào một Data Lakehouse cục bộ (local) và được xử lý, biến đổi để phục vụ cho mục đích báo cáo phân tích. Dự án này cũng tích hợp thêm yếu tố AI để phân loại sản phẩm.

**Mục tiêu chính:**
- Hiểu và áp dụng mô hình ELT (Extract, Load, Transform).
- Làm quen với kiến trúc Medallion (Bronze - Silver - Gold).
- Sử dụng các công cụ Data Engineering hiện đại nhưng nhẹ và miễn phí: **Python, dbt, DuckDB**.

---

## 2. Công nghệ sử dụng (Tech Stack)
- **Ngôn ngữ lập trình:** Python (dùng để Extract & Load dữ liệu từ API và tạo dữ liệu CSV giả lập).
- **Cơ sở dữ liệu (Database / Data Warehouse):** DuckDB (Database phân tích OLAP, chạy local bằng file, siêu nhanh và không cần cài đặt server).
- **Công cụ Biến đổi dữ liệu (Transformation):** dbt (Data Build Tool) kết hợp với DuckDB, sử dụng SQL để transform dữ liệu theo các lớp (Staging, Marts).
- **AI / Machine Learning:** Sử dụng API của các LLM (như OpenAI API) hoặc một mô hình phân loại quy mô nhỏ (rule-based giả lập) trong Python để tự động gán nhãn danh mục sản phẩm, đảm bảo dự án chạy mượt mà trên máy cá nhân mà không cần tải mô hình hàng GB.

---

## 3. Kiến trúc luồng dữ liệu (Data Flow / Pipeline)
Theo kiến trúc **Medallion**:

1. **Nguồn Dữ liệu (Source):** Dữ liệu đơn hàng, khách hàng (CSV), dữ liệu tỷ giá (JSON API).
2. **Lớp Raw (Dữ liệu thô):** Lưu nguyên bản các file tải về vào thư mục `data/raw/`.
3. **Lớp Bronze (Staging):** Nạp dữ liệu thô từ CSV/JSON vào DuckDB mà không thay đổi logic.
4. **Lớp Silver (Intermediate):** Làm sạch dữ liệu, chuẩn hóa tên cột, chuyển đổi kiểu dữ liệu. Bước đầu xây dựng các cấu trúc cơ bản trước khi đưa vào kho dữ liệu.
5. **Lớp Gold (Marts / Analytics):** Tổ chức dữ liệu theo **Mô hình Sao (Star Schema)**. Lớp này sẽ chứa:
   - **Bảng Fact (Sự kiện trung tâm):** `fct_orders` (chi tiết từng giao dịch mua hàng, đã quy đổi VND sang USD bằng tỷ giá API).
   - **Bảng Dimension (Chiều phân tích):** `dim_customers` (thông tin khách hàng), `dim_products` (thông tin sản phẩm, kèm nhãn danh mục được tạo bởi AI).
   - **Bảng Báo cáo (Aggregated Marts):** `mart_sales_daily`, `mart_sales_by_category`.

---

## 4. Cấu trúc thư mục (Directory Structure)
Dưới đây là cấu trúc chính của dự án. File này được dùng để các AI model khác hiểu được toàn bộ context khi đọc vào dự án:

```text
[Thư mục dự án: ecommerce_lakehouse]/
├── PROJECT_CONTEXT.md         # File ghi nhận lại thông tin tổng quan của toàn bộ dự án này
├── data/
│   └── raw/                   # Chứa dữ liệu CSV tải về và file JSON từ API
├── database/                  # Thư mục lưu trữ file database của DuckDB (ví dụ: ecom.duckdb)
├── dbt_ecommerce/             # Thư mục chứa project dbt dùng để transform dữ liệu trong DuckDB
├── scripts/
│   ├── 01_generate_data.py    # Sinh dữ liệu CSV mẫu (Khách hàng, Đơn hàng, Sản phẩm)
│   ├── 02_fetch_api.py        # Gọi API lấy tỷ giá tiền tệ (ví dụ: VND -> USD)
│   ├── 03_ai_categorize.py    # Dùng Python/API phân loại sản phẩm và lưu ra CSV
│   └── 04_load_to_duckdb.py   # Load toàn bộ dữ liệu từ thư mục `data/raw` vào lớp Bronze của DuckDB
├── requirements.txt           # Danh sách các thư viện Python cần cài
└── README.md
```

---

## 5. Quy trình thực hiện (Roadmap / Todo List)

- [x] **Giai đoạn 1: Khởi tạo & Môi trường**
  - [x] Tạo file `requirements.txt` với các thư viện: `pandas`, `requests`, `duckdb`, `dbt-duckdb`, `python-dotenv`.
  - [x] Khởi tạo cấu trúc thư mục (`data/raw`, `database`, `scripts`).
- [ ] **Giai đoạn 2: Extract & Load (Python)**
  - [ ] Viết script `01_generate_data.py` sinh dữ liệu CSV.
  - [ ] Viết script `02_fetch_api.py` gọi API lấy tỷ giá.
  - [ ] Viết script `03_ai_categorize.py` gắn mác sản phẩm bằng AI/Logic.
  - [ ] Viết script `04_load_to_duckdb.py` đẩy dữ liệu vào `database/ecom.duckdb`.
- [ ] **Giai đoạn 3: Transform (dbt)**
  - [ ] Thiết lập dbt project (`dbt_ecommerce`) và cấu hình `profiles.yml` trỏ đến `ecom.duckdb`.
  - [ ] Viết các model SQL cho lớp Bronze (Staging/Làm sạch).
  - [ ] Viết các model SQL cho lớp Silver (Kết hợp dữ liệu Fact & Dimension).
  - [ ] Viết các model SQL cho lớp Gold (Báo cáo doanh thu cuối cùng).
- [ ] **Giai đoạn 4: Hoàn thiện & Tài liệu**
  - [ ] Chạy pipeline end-to-end.
  - [ ] Viết file `README.md` hướng dẫn chạy dự án cho người mới.

---

## 6. Quản lý Version Control (Git/GitHub)
Mỗi khi có sự thay đổi về dự án (ví dụ: hoàn thành một script, một giai đoạn hoặc cập nhật tài liệu), dự án sẽ được **commit và push lên GitHub**. Việc này giúp:
- Theo dõi lịch sử thay đổi rõ ràng.
- Ghi nhận tiến độ hoàn thành dự án qua từng bước.
- Lưu trữ an toàn mã nguồn.

---
*Lưu ý cho AI Assistant: Khi bắt đầu session mới, hãy đọc file này đầu tiên để nắm rõ bối cảnh, cấu trúc và tiến độ của dự án, nhằm tiết kiệm context token và đảm bảo đi đúng hướng.*
