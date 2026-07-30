# 📖 DATA DICTIONARY & FIELD CATALOG
**Project:** ASEAN Socio-Economic & Development Analysis (2015 - 2025)  
**Schema Architecture:** 3-Tier Star Schema  

---

## 📌 1. BẢNG SỰ KIỆN CHÍNH: `Fact_ASEAN_Indicators`
**Tệp tin:** `02_Data/Cleaned/Fact_ASEAN_Indicators.csv`  
**Hạt dữ liệu (Grain):** 1 bản ghi duy nhất cho mỗi tổ hợp `(CountryCode, SeriesCode, Year)`  
**Số dòng:** 6,730 bản ghi sạch (Null values removed)  

| Tên Cột | Kiểu Dữ Liệu | Khóa (PK/FK) | Mô Tả Chi Tiết | Ví Dụ Mẫu | Quy Tắc Aggregation DAX |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `CountryCode` | Text (String) | **FK** | Mã ISO 3166-1 alpha-3 của quốc gia | `VNM`, `IDN`, `SGP` | N/A (Group by Dimension) |
| `SeriesCode` | Text (String) | **FK** | Mã chỉ số định danh từ World Bank | `NY.GDP.MKTP.CD` | N/A (Filter by Dimension) |
| `Year` | Integer (Int64) | **FK** | Năm ghi nhận chỉ số (2015 đến 2025) | `2015`, `2023` | N/A (Join with Dim_Date) |
| `Value` | Decimal (Float64) | - | Giá trị định lượng của chỉ số phát triển | `433810000000.0` | `SUM()`, `AVERAGE()` |

---

## ✈️ 2. BẢNG SỰ KIỆN LUỒNG DU LỊCH: `Fact_ASEAN_Tourism_Flow`
**Tệp tin:** `02_Data/Cleaned/Fact_ASEAN_Tourism_Flow.csv`  
**Hạt dữ liệu (Grain):** 1 bản ghi duy nhất cho mỗi luồng di chuyển `(DestinationCountryCode, OriginCountryCode, Year)`  
**Số dòng:** 917 bản ghi  

| Tên Cột | Kiểu Dữ Liệu | Khóa (PK/FK) | Mô Tả Chi Tiết | Ví Dụ Mẫu |
| :--- | :--- | :---: | :--- | :--- |
| `DestinationCountryCode` | Text | **FK** | Mã ISO3 của quốc gia Đích (Nơi nhập cảnh) | `MYS`, `THA`, `SGP` |
| `OriginCountryCode` | Text | **FK** | Mã ISO3 của quốc gia Nguồn (Nơi xuất phát) | `SGP`, `IDN`, `VNM` |
| `Year` | Integer | **FK** | Năm ghi nhận lượt khách du lịch | `2019`, `2023` |
| `Visitors` | Decimal | - | Số lượt khách du lịch nhập cảnh | `8308230.0` |

---

## 🌏 3. BẢNG CHIỀU QUỐC GIA: `Dim_Country`
**Tệp tin:** `02_Data/Cleaned/Dim_Country.csv`  
**Số dòng:** 11 bản ghi (10 nước ASEAN + Timor-Leste)  

| Tên Cột | Kiểu Dữ Liệu | Khóa | Mô Tả Chi Tiết | Power BI Data Category |
| :--- | :--- | :---: | :--- | :--- |
| `CountryCode` | Text | **PK** | Mã ISO3 duy nhất làm khóa chính | Uncategorized (Key) |
| `CountryName` | Text | - | Tên quốc gia đầy đủ bằng tiếng Anh | `Country/Region` |
| `SubRegion` | Text | - | Phân loại tiểu vùng: `Mainland ASEAN` vs `Maritime ASEAN` | Region |
| `Capital` | Text | - | Thủ đô của quốc gia | City |
| `ISO2` | Text | - | Mã ISO 2 ký tự | Uncategorized |
| `Latitude` | Decimal | - | Tọa độ vĩ độ tâm quốc gia | `Latitude` |
| `Longitude` | Decimal | - | Tọa độ kinh độ tâm quốc gia | `Longitude` |

---

## 📋 4. BẢNG CHIỀU CHỈ SỐ: `Dim_Indicator`
**Tệp tin:** `02_Data/Cleaned/Dim_Indicator.csv`  
**Số dòng:** 65 bản ghi  

| Tên Cột | Kiểu Dữ Liệu | Khóa | Mô Tả Chi Tiết | Ví Dụ Mẫu |
| :--- | :--- | :---: | :--- | :--- |
| `SeriesCode` | Text | **PK** | Mã chỉ số định danh World Bank | `IT.NET.USER.ZS` |
| `SeriesName` | Text | - | Tên đầy đủ của chỉ số phát triển | `Individuals using the Internet (% of population)` |
| `Domain` | Text | - | 1 trong 10 mảng phát triển trọng yếu | `Công nghệ & Hạ tầng số` |
| `UnitOfMeasure` | Text | - | Đơn vị tính bóc tách từ tên chỉ số | `%`, `current US$`, `Person` |

---

## 📅 5. BẢNG CHIỀU THỜI GIAN: `Dim_Date`
**Tệp tin:** `02_Data/Cleaned/Dim_Date.csv`  
**Số dòng:** 11 bản ghi (2015 đến 2025)  

| Tên Cột | Kiểu Dữ Liệu | Khóa | Mô Tả Chi Tiết | Sử Dụng Trong DAX |
| :--- | :--- | :---: | :--- | :--- |
| `Year` | Integer | **PK** | Năm (Khóa liên kết) | `Dim_Date[Year]` |
| `Date` | Date | - | Ngày đầu năm (`YYYY-01-01`) | Mark as Date Table (`SAMEPERIODLASTYEAR`) |
| `YearLabel` | Text | - | Nhãn năm hiển thị visual | `Năm 2015`, `Năm 2023` |
| `Decade` | Text | - | Thập kỷ | `Thập kỷ 2010s`, `Thập kỷ 2020s` |
| `Period` | Text | - | Giai đoạn 5 năm | `2015-2020` vs `2021-2025` |
