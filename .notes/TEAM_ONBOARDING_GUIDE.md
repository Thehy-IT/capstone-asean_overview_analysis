# 🚀 HƯỚNG DẪN BẮT ĐẦU CHO THÀNH VIÊN MỚI (TEAM ONBOARDING GUIDE)
**Dự án:** Phân Tích Xu Hướng Phát Triển Kinh Tế - Xã Hội Khối ASEAN (2015 - 2025)  
**Tài liệu dành cho:** Thành viên mới gia nhập team (Dễ hiểu, đầy đủ, từng bước một).

---

## 📌 1. TỔNG QUAN DỰ ÁN

Dự án này thực hiện **thu thập, làm sạch, phân tích và trực quan hóa dữ liệu vĩ mô** của 11 quốc gia khu vực Đông Nam Á (10 nước thành viên ASEAN + Timor-Leste) trong giai đoạn 10 năm (2015–2025).

Dữ liệu bao phủ **10 mảng phát triển trọng yếu**:
1. Kinh tế & GDP
2. Dân số & Nhân khẩu học
3. Du lịch & Dịch vụ
4. Đầu tư trực tiếp nước ngoài (FDI)
5. Giáo dục & Đào tạo
6. Công nghệ & Hạ tầng số
7. Lao động & Việc làm
8. Y tế & Sức khỏe
9. Môi trường & Năng lượng
10. Thương mại & Xuất nhập khẩu

---

## 📁 2. BẢN ĐỒ CẤU TRÚC DỰ ÁN (SITEMAP)

Dự án được sắp xếp theo đúng thứ tự 8 bước vận hành:

| Thư mục | Chức năng & Vai trò |
| :--- | :--- |
| 📄 `01_Project_Document/` | Đề cương, Báo cáo chính thức (`Final_Report.docx`), Slide thuyết trình (`Presentation.pptx`). |
| 🗄️ `02_Data/` | **Kho dữ liệu 3 tầng**: `Raw` (Dữ liệu thô), `Cleaned` (Dữ liệu sạch Star Schema), `Metadata` (Từ điển dữ liệu). |
| ⚙️ `03_Data_Preprocessing/` | Script nạp dữ liệu: `PowerQuery/Load_Star_Schema.m` và SQL `SQL/create_tables_and_views.sql`. |
| 📊 `04_Analysis/` | Kết quả phân tích: Jupyter Notebook (`EDA.ipynb`), Báo cáo `Insights.md`, Excel tổng hợp. |
| 📈 `05_PowerBI/` | Bộ mã DAX Enterprise (`Dataset/DAX_Measures.dax`), Theme giao diện tối (`Theme/`). |
| 🖼️ `06_Images/` | Kho đồ thị phân loại: `Overview_Trends/`, `Quality_Audit/`, `EDA_Plots/`. |
| 📸 `07_Dashboard_Screenshots/` | Ảnh chụp giao diện Dashboard Power BI. |
| 💻 `08_Source_Code/` | **Mã nguồn Production**: `main.py` và gói `src/` làm sạch dữ liệu tự động. |

---

## 🚀 3. HƯỚNG DẪN 3 BƯỚC BẮT ĐẦU CHẠY DỰ ÁN (QUICK START)

### 🔹 BƯỚC 1: Chạy Pipeline Tự Động Làm Sạch & Kiểm Thử Dữ Liệu (Python)
Mở terminal tại thư mục gốc của dự án và chạy duy nhất 1 câu lệnh:

```bash
python 08_Source_Code/main.py
```

**Chương trình sẽ tự động thực hiện 3 công việc:**
1. Đọc dữ liệu thô từ `02_Data/Raw/` -> Làm sạch & Đưa về dạng Star Schema trong `02_Data/Cleaned/`.
2. Chạy bộ tự động kiểm thử dữ liệu (CI/CD Unit Tests) kiểm tra khóa chính, khóa ngoại, zero-duplicate.
3. Tạo file Notebook phân tích `04_Analysis/EDA.ipynb`.

---

### 🔹 BƯỚC 2: Khởi Tạo Cơ Sở Dữ Liệu SQL (Nếu Dùng SQL)
Nếu bạn muốn truy vấn phân tích bằng SQL:
* Sử dụng file kịch bản SQL: `03_Data_Preprocessing/SQL/create_tables_and_views.sql`
* Chạy kịch bản này trên PostgreSQL, SQLite, MySQL hoặc SQL Server để tạo 5 bảng Star Schema và các View phân tích GDP / Công nghệ.

---

### 🔹 BƯỚC 3: Mở & Xây Dựng Power BI Dashboard
Nếu bạn phụ trách làm Dashboard Power BI:
1. **Import Dữ liệu**: Mở Power BI Desktop -> Vào `Get Data` -> `Blank Query` -> Mở `Advanced Editor` -> Copy toàn bộ mã M-code trong file `03_Data_Preprocessing/PowerQuery/Load_Star_Schema.m` dán vào.
2. **Nạp Mã DAX**: Đã có sẵn 50+ DAX Measures chuẩn Enterprise trong file `05_PowerBI/Dataset/DAX_Measures.dax`. Bạn chỉ cần copy/paste mã DAX vào Power BI.
3. **Áp dụng Theme Giao diện Tối**: Trong Power BI -> Thẻ `View` -> `Browse for themes` -> Chọn file `05_PowerBI/Theme/ASEAN_Dark_Professional_Theme.json`.

---

## 🧠 4. HIỂU VỀ MÔ HÌNH DỮ LIỆU STAR SCHEMA

Dữ liệu được tổ chức theo chuẩn **Star Schema (Mô hình Ngôi sao)** gồm:

* **3 Bảng Chiều (Dimension Tables):**
  1. `Dim_Country`: Chứa thông tin 11 quốc gia (Tên, Thủ đô, Tọa độ, Tiểu vùng, Trạng thái thành viên).
  2. `Dim_Indicator`: Chứa danh mục 66 chỉ số (Tên chỉ số, Miền phát triển, Đơn vị đo).
  3. `Dim_Date`: Chứa thời gian 2015–2025 (Năm, Trạng thái Actual/Forecast).

* **2 Bảng Thực Thể (Fact Tables):**
  1. `Fact_ASEAN_Indicators`: Lưu toàn bộ giá trị chỉ số kinh tế - xã hội (`Value`).
  2. `Fact_ASEAN_Tourism_Flow`: Lưu luồng du khách di chuyển giữa các nước (`Destination`, `Origin`, `Visitors`).

---

## 📖 5. CÁC TÀI LIỆU PHẢI ĐỌC DÀNH CHO THÀNH VIÊN MỚI

1. **Từ Điển Dữ Liệu**: Đọc `02_Data/Metadata/Data_Dictionary.md` để hiểu ý nghĩa 66 chỉ số World Bank.
2. **Báo Cáo Insight Vĩ Mô**: Đọc `04_Analysis/Insights.md` để nắm các phát hiện chính về GDP, lạm phát, du lịch.
3. **Quy Chuẩn DAX**: Đọc `05_PowerBI/Dataset/DAX_Measures.dax` để hiểu cách tính tăng trưởng YoY, xếp hạng Rank ASEAN và KPI Flag.

---

## ❓ FAQ & XỬ LÝ LỖI THƯỜNG GẶP

* **Q: Bị lỗi thiếu thư viện Python khi chạy `main.py`?**
  * *Trả lời*: Cài đặt nhanh các thư viện bằng câu lệnh:
    ```bash
    pip install pandas numpy matplotlib seaborn
    ```
* **Q: Tôi muốn đóng góp code/feature mới thì làm như thế nào?**
  * *Trả lời*: Viết kịch bản mới trong folder `08_Source_Code/src/` và thêm bước gọi trong `08_Source_Code/main.py`.

---
*Chúc bạn có trải nghiệm làm việc tuyệt vời cùng team với dự án Capstone ASEAN! 🚀*
