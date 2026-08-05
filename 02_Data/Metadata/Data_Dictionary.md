# TỪ ĐIỂN DỮ LIỆU VÀ DANH MỤC THUỘC TÍNH MÔ HÌNH NGÔI SAO (ENTERPRISE DATA DICTIONARY)

**Dự án:** Phân tích Phát triển Kinh tế - Xã hội ASEAN (2015 – 2025)  
**Kiến trúc Mô hình:** Mô hình Ngôi sao 3 Lớp (3-Tier Star Schema Architecture)  
**Thư mục lưu trữ:** `02_Data/Cleaned/`  
**Đơn vị quản trị:** Bộ phận Data Engineering & Analytics Architecture  
**Phiên bản tài liệu:** 2.0 (Chuẩn Kiểm định Doanh nghiệp)  

---

## I. TỔNG QUAN KIẾN TRÚC MÔ HÌNH DỮ LIỆU

Từ điển dữ liệu này mô tả chi tiết các thuộc tính, hạt nhân dữ liệu (Grain), kiểu dữ liệu, các ràng buộc khóa chính/khóa ngoại và quy tắc gom nhóm DAX/SQL cho 5 bảng sạch thuộc Mô hình Ngôi sao (Star Schema) cùng bảng Master đối soát.

| Tên Bảng (Entity Name) | Phân Loại Bảng | Hạt Dữ Liệu (Grain) | Số Dòng | Tệp Lưu Trữ |
| :--- | :--- | :--- | ---:| :--- |
| **Fact_ASEAN_Indicators** | Bảng Sự kiện Chính | `(CountryCode, SeriesCode, Year)` duy nhất | 6,730 | `Fact_ASEAN_Indicators.csv` |
| **Fact_ASEAN_Tourism_Flow** | Bảng Sự kiện Luồng | `(DestinationCountryCode, OriginCountryCode, Year)` duy nhất | 908 | `Fact_ASEAN_Tourism_Flow.csv` |
| **Dim_Country** | Bảng Chiều Quốc gia | 1 dòng / `CountryCode` (Mã ISO3 duy nhất) | 11 | `Dim_Country.csv` |
| **Dim_Indicator** | Bảng Chiều Chỉ số | 1 dòng / `SeriesCode` (Mã chỉ số duy nhất) | 65 | `Dim_Indicator.csv` |
| **Dim_Date** | Bảng Chiều Thời gian | 1 dòng / `Year` (Năm duy nhất 2015 - 2025) | 11 | `Dim_Date.csv` |
| **ASEAN_Master_Cleaned** | Bảng Tổng hợp Master | 1 dòng / `(CountryCode, SeriesCode, Year)` dạng phẳng | 7,850 | `ASEAN_Master_Cleaned.csv` |

---

## II. CHI TIẾT CÁC BẢNG SỰ KIỆN (FACT TABLES)

### 1. Bảng Sự kiện Chỉ số Vĩ mô: `Fact_ASEAN_Indicators`
- **Tệp lưu trữ:** `02_Data/Cleaned/Fact_ASEAN_Indicators.csv`
- **Mô tả:** Chứa các bản ghi dữ liệu định lượng của 65 chỉ số vĩ mô đã qua làm sạch, bỏ giá trị khuyết rỗng và unpivot sang dạng dọc (Long Format).
- **Hạt dữ liệu (Grain):** Mỗi dòng biểu diễn 1 giá trị đo lường duy nhất của 1 chỉ số tại 1 quốc gia trong 1 năm cụ thể.

| Tên Thuộc Tính | Kiểu Dữ Liệu | Khóa | Ràng Buộc Null | Mô Tả Diễn Giải | Giá Trị Mẫu | Quy Tắc DAX Aggregation |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| `CountryCode` | Text (String) | **FK** | Not Null | Mã định danh ISO 3166-1 alpha-3 của quốc gia | `VNM`, `IDN`, `SGP` | Khóa ngoại trỏ đến `Dim_Country[CountryCode]` |
| `SeriesCode` | Text (String) | **FK** | Not Null | Mã chỉ số định danh quốc tế từ World Bank | `NY.GDP.MKTP.CD` | Khóa ngoại trỏ đến `Dim_Indicator[SeriesCode]` |
| `Year` | Integer (Int64) | **FK** | Not Null | Năm ghi nhận dữ liệu chỉ số (2015 – 2025) | `2015`, `2023` | Khóa ngoại trỏ đến `Dim_Date[Year]` |
| `Value` | Decimal (Float64) | - | Not Null | Giá trị đo lường định lượng của chỉ số | `433810000000.0` | `SUM()` đối với biến tuyệt đối, `AVERAGE()` đối với tỷ lệ % |

---

### 2. Bảng Sự kiện Luồng Du lịch Nội khối: `Fact_ASEAN_Tourism_Flow`
- **Tệp lưu trữ:** `02_Data/Cleaned/Fact_ASEAN_Tourism_Flow.csv`
- **Mô tả:** Chứa ma trận hai chiều về lưu lượng lượt khách du lịch quốc tế nhập cảnh giữa 11 quốc gia nguồn và đích trong khu vực ASEAN.
- **Hạt dữ liệu (Grain):** Mỗi dòng biểu diễn tổng lượt khách di chuyển từ 1 quốc gia xuất phát (Origin) đến 1 quốc gia điểm đến (Destination) trong 1 năm.

| Tên Thuộc Tính | Kiểu Dữ Liệu | Khóa | Ràng Buộc Null | Mô Tả Diễn Giải | Giá Trị Mẫu | Quy Tắc DAX / Context |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| `DestinationCountryCode` | Text (String) | **FK** | Not Null | Mã ISO3 của quốc gia Đích (Nơi du khách nhập cảnh) | `MYS`, `THA`, `SGP` | Active Relationship với `Dim_Country[CountryCode]` |
| `OriginCountryCode` | Text (String) | **FK** | Not Null | Mã ISO3 của quốc gia Nguồn (Nơi du khách xuất phát) | `SGP`, `IDN`, `VNM` | Role-Playing Relationship (`USERELATIONSHIP`) |
| `Year` | Integer (Int64) | **FK** | Not Null | Năm ghi nhận luồng du lịch (2016 – 2025) | `2019`, `2023` | Khóa ngoại trỏ đến `Dim_Date[Year]` |
| `Visitors` | Decimal (Float64) | - | Not Null | Tổng số lượt khách du lịch di chuyển (người) | `8308230.0` | `SUM(Visitors)` |

---

## III. CHI TIẾT CÁC BẢNG CHIỀU (DIMENSION TABLES)

### 1. Bảng Chiều Quốc gia: `Dim_Country`
- **Tệp lưu trữ:** `02_Data/Cleaned/Dim_Country.csv`
- **Mô tả:** Danh mục thông tin định danh quốc gia, thông tin phân vùng địa lý, tọa độ GIS và ghi chú đặc thù dữ liệu.

| Tên Thuộc Tính | Kiểu Dữ Liệu | Khóa | Power BI Category | Mô Tả Diễn Giải | Giá Trị Mẫu |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `CountryCode` | Text (String) | **PK** | Uncategorized | Mã ISO3 3 ký tự duy nhất đại diện quốc gia | `VNM`, `SGP`, `TLS` |
| `CountryName` | Text (String) | - | Country/Region | Tên quốc gia đầy đủ bằng tiếng Anh | `Viet Nam`, `Singapore` |
| `SubRegion` | Text (String) | - | Region | Phân loại tiểu vùng: `Mainland ASEAN` vs `Maritime ASEAN` | `Mainland ASEAN` |
| `Capital` | Text (String) | - | City | Tên thủ đô của quốc gia | `Hanoi`, `Singapore` |
| `ISO2` | Text (String) | - | Uncategorized | Mã ISO 3166-1 alpha-2 hai ký tự | `VN`, `SG`, `ID` |
| `Latitude` | Decimal (Float64) | - | Latitude | Tọa độ vĩ độ tâm địa lý quốc gia (GIS Mapping) | `14.0583` |
| `Longitude` | Decimal (Float64) | - | Longitude | Tọa độ kinh độ tâm địa lý quốc gia (GIS Mapping) | `108.2772` |
| `MemberStatus` | Text (String) | - | Uncategorized | Trạng thái thành viên: `Full Member` vs `Observer Candidate` | `Full Member` |
| `DataNote` | Text (String) | - | Uncategorized | Ghi chú đặc thù về chất lượng và biến động dữ liệu | `High-income city-state` |

---

### 2. Bảng Chiều Chỉ số: `Dim_Indicator`
- **Tệp lưu trữ:** `02_Data/Cleaned/Dim_Indicator.csv`
- **Mô tả:** Danh mục mã hóa 65 chỉ số phát triển kinh tế - xã hội, tên tiếng Anh chính thức, nhóm mảng phân loại và đơn vị tính.

| Tên Thuộc Tính | Kiểu Dữ Liệu | Khóa | Mô Tả Diễn Giải | Giá Trị Mẫu |
| :--- | :--- | :---: | :--- | :--- |
| `SeriesCode` | Text (String) | **PK** | Mã chỉ số chuẩn quốc tế từ ngân hàng dữ liệu World Bank | `IT.NET.USER.ZS`, `NY.GDP.MKTP.CD` |
| `SeriesName` | Text (String) | - | Tên tiếng Anh đầy đủ của chỉ số | `Individuals using the Internet (% of population)` |
| `Domain` | Text (String) | - | 1 trong 10 mảng phát triển kinh tế - xã hội trọng yếu | `Công nghệ & Hạ tầng số` |
| `UnitOfMeasure` | Text (String) | - | Đơn vị tính bóc tách chuẩn từ tên chỉ số | `% of population`, `current US$`, `years` |

---

### 3. Bảng Chiều Thời gian: `Dim_Date`
- **Tệp lưu trữ:** `02_Data/Cleaned/Dim_Date.csv`
- **Mô tả:** Danh mục chuỗi thời gian 11 năm (2015 – 2025) phục vụ phân tích xu hướng và tính toán Time Intelligence theo độ mịn hạt năm.

| Tên Thuộc Tính | Kiểu Dữ Liệu | Khóa | Mô Tả Diễn Giải | Vai Trò Trong DAX / Power BI | Giá Trị Mẫu |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `Year` | Integer (Int64) | **PK** | Khóa số nguyên năm duy nhất (2015 – 2025) | Khóa liên kết `1:N` với các bảng Fact | `2015`, `2023` |
| `Date` | Date | - | Ngày đại diện đầu năm dạng ISO `YYYY-01-01` | Hạt nhân Năm (`Annual Grain`) | `2015-01-01` |
| `YearLabel` | Text (String) | - | Nhãn năm định dạng hiển thị trực quan | Dùng làm nhãn trục trên biểu đồ | `Năm 2015`, `Năm 2023` |
| `Decade` | Text (String) | - | Phân loại thập kỷ | Dùng làm slicer lọc cấp cao | `Thập kỷ 2010s`, `Thập kỷ 2020s` |
| `Period` | Text (String) | - | Phân loại giai đoạn 5 năm | Dùng phân nhóm đối sánh | `2015-2020` vs `2021-2025` |
| `DataStatus` | Text (String) | - | Trạng thái dữ liệu: `Actual`, `Preliminary`, `Forecast` | Đánh dấu độ tin cậy số liệu | `Actual`, `Forecast/Incomplete` |
| `IsCurrentYear` | Boolean | - | Cờ đánh dấu năm cuối cùng của dải phân tích | Dùng lọc mặc định trong KPI Card | `True`, `False` |

---

## IV. BẢNG TỔNG HỢP MASTER DÙNG CHO ĐỐI SOÁT: `ASEAN_Master_Cleaned`

- **Tệp lưu trữ:** `02_Data/Cleaned/ASEAN_Master_Cleaned.csv`
- **Số dòng:** 7,850 bản ghi (gồm cả các bản ghi rỗng để kiểm định tỷ lệ khuyết thiếu)
- **Mục tiêu:** Cung cấp góc nhìn phẳng (Denormalized Flat Table) phục vụ việc audit, đối soát dữ liệu nhanh trên Python / Excel / SQL mà không cần viết lệnh JOIN.

| Tên Thuộc Tính | Kiểu Dữ Liệu | Mô Tả Diễn Giải | Ví Dụ Mẫu |
| :--- | :--- | :--- | :--- |
| `CountryName` | Text | Tên quốc gia đầy đủ bằng tiếng Anh | `Viet Nam` |
| `CountryCode` | Text | Mã ISO3 của quốc gia | `VNM` |
| `SeriesName` | Text | Tên đầy đủ của chỉ số phát triển | `GDP (current US$)` |
| `SeriesCode` | Text | Mã chỉ số định danh World Bank | `NY.GDP.MKTP.CD` |
| `Domain` | Text | Mảng phát triển thuộc chỉ số | `Kinh tế & GDP` |
| `Year` | Integer | Năm ghi nhận dữ liệu | `2023` |
| `Value` | Decimal / Null | Giá trị chỉ số (chứa cả rỗng `""` phục vụ kiểm tra missing rate) | `433810000000.0` |

---

## V. NGUYÊN TẮC QUẢN TRỊ VÀ QUY TẮC TỔNG HỢP NĂNG LỰC DAX

1. **Ràng buộc Duy nhất (Uniqueness Integrity):**
   - `Dim_Country[CountryCode]` là khóa chính duy nhất (0% trùng lặp).
   - `Dim_Indicator[SeriesCode]` là khóa chính duy nhất (0% trùng lặp).
   - `Dim_Date[Year]` là khóa chính duy nhất (0% trùng lặp).
   - Khóa tổ hợp `(CountryCode, SeriesCode, Year)` trong `Fact_ASEAN_Indicators` đảm bảo tính duy nhất hạt dữ liệu.

2. **Quy tắc Gom nhóm Số liệu (Aggregation Semantics):**
   - **Chỉ số Giá trị Tuyệt đối (Stock/Flow Absolute Values):** Sử dụng hàm `SUM()` để tính tổng toàn khối ASEAN (ví dụ: GDP, Dân số, Kim ngạch Xuất nhập khẩu).
   - **Chỉ số Tỷ lệ phần trăm (% GDP, % Dân số, % Lao động):** Sử dụng hàm `AVERAGE()` hoặc tính Trung bình Gia quyền (Weighted Average), **tuyệt đối không dùng `SUM()`** để tránh sai lệch bản chất tỷ lệ.
   - **Chỉ số Mật độ (Thuê bao/100 dân, Giường bệnh/1.000 dân):** Sử dụng hàm `AVERAGE()`.

---

**Tài liệu được thẩm định bởi:** Bộ phận Kiểm định Kiến trúc Dữ liệu Dự án ASEAN Overview Analysis  
**Trạng thái tuân thủ:** Đã xác minh khớp 100% với tệp CSV thực tế tại thư mục `02_Data/Cleaned/`.
