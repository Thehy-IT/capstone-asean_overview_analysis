# BÁO CÁO PHÂN TÍCH KHÁM PHÁ CHUYÊN SÂU (SENIOR EDA REPORT)
**Dự án:** Phân tích Tổng quan Phát triển Các nước ASEAN (2015 - 2025)  
**Tác giả:** Senior Data Analyst & BI Solution Architect (20 năm kinh nghiệm)  

---

## 🎯 EXECUTIVE SUMMARY & NỔI BẬT ĐỊNH LƯỢNG (KEY NUMERICAL INSIGHTS)

Dựa trên dữ liệu 7,647 bản ghi sạch đã kiểm định từ World Bank, báo cáo khám phá chuyên sâu ghi nhận **3 phát hiện chiến lược** về xu hướng kinh tế, chuyển đổi số và dòng dịch chuyển dịch vụ trong khối ASEAN (2015–2023):

---

## 💰 1. QUI MÔ GDP & ĐỘ TẬP TRUNG KINH TẾ (ECONOMIC CONCENTRATION)

- **Quy mô GDP Toàn khối ASEAN:** Tăng trưởng từ **2,530 tỷ USD (năm 2015)** lên **3,262 tỷ USD (năm 2019)** và đạt mốc lịch sử **3,812 tỷ USD (năm 2023)**.
- **Độ tập trung Top 3:** 3 nền kinh tế lớn nhất bao gồm Indonesia (`IDN`), Thailand (`THA`), và Singapore (`SGP`) liên tục chiếm giữ **~62.5% đến 62.9%** tổng quy mô GDP của cả khu vực ASEAN.
- **Sự vươn lên của Việt Nam:** Việt Nam (`VNM`) đạt quy mô GDP **433.81 tỷ USD (năm 2023)**, chính thức vươn lên vị trí thứ 5 toàn khu vực, tiệm cận Philippines ($437.06B) và Singapore ($511.18B).

| Quốc gia | GDP 2015 (USD) | GDP 2019 (USD) | GDP 2023 (USD) | Tỷ trọng 2023 (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Indonesia** | $860.85 Billion | $1,119.10 Billion | **$1,371.17 Billion** | **35.97%** |
| **Thailand** | $401.30 Billion | $543.98 Billion | **$517.01 Billion** | **13.56%** |
| **Singapore** | $308.00 Billion | $376.83 Billion | **$511.18 Billion** | **13.41%** |
| **Philippines** | $306.45 Billion | $376.82 Billion | **$437.06 Billion** | **11.46%** |
| **Viet Nam** | $239.26 Billion | $334.36 Billion | **$433.81 Billion** | **11.38%** |

---

## 🚀 2. BƯỚC NHẢY CHUYỂN ĐỔI SỐ (DIGITAL LEAPFROGGING)

Tỷ lệ người dùng Internet (% Dân số) ghi nhận sự bứt phá thần tốc ở nhóm các quốc gia đang phát triển:

1. **Cambodia (`KHM`):** Bứt phá kỷ lục toàn khối với mức tăng **+62.49 điểm %** (từ 6.43% năm 2015 lên 68.93% năm 2023).
2. **Thailand (`THA`):** Tăng **+50.22 điểm %** (từ 39.32% lên 89.54%).
3. **Indonesia (`IDN`):** Tăng **+47.15 điểm %** (từ 22.06% lên 69.21%).
4. **Lao PDR (`LAO`):** Tăng **+46.20 điểm %** (từ 18.20% lên 64.40%).
5. **Viet Nam (`VNM`):** Đạt mốc **78.08%** bao phủ Internet năm 2023.

---

## ✈️ 3. HÀNH LAN DU LỊCH NỘI KHỐI (INTRA-ASEAN TOURISM CORRIDORS)

Phân tích ma trận luồng di chuyển khách du lịch (`Fact_ASEAN_Tourism_Flow`) cho thấy các hành lang du lịch sôi động nhất khối ASEAN:

- **Hành lang 1 (Singapore $\rightarrow$ Malaysia):** Đạt đỉnh 10.16 triệu lượt khách (năm 2019) và phục hồi đạt 8.31 triệu lượt khách (năm 2023).
- **Hành lang 2 (Malaysia $\rightarrow$ Thailand):** Vượt mốc trước dịch, đạt **4.63 triệu lượt khách (năm 2023)** so với 4.27 triệu lượt (năm 2019).
- **Hành lang 3 (Indonesia $\rightarrow$ Malaysia):** Phục hồi đạt **3.11 triệu lượt khách (năm 2023)**.

---

## 💡 ĐỀ XUẤT THIẾT KẾ DASHBOARD CHO POWER BI

1. **Trang 1 - Overview KPI (Toàn cảnh ASEAN):**
   - KPI Card: Tổng GDP toàn khối ($3.81 Trillion USD), Tỷ lệ Bao phủ Internet Trung bình (62.5%), Tổng Dân số (680M+).
   - Treemap Visual: Tỷ trọng GDP các nước trong khối ASEAN.

2. **Trang 2 - Digital & Social Transformation (Số hóa & Xã hội):**
   - Slope Chart / Line Chart: Xu hướng tăng trưởng Internet % từ 2015 đến 2023 của 10 nước.

3. **Trang 3 - International Tourism Flow (Luồng Du lịch Nội khối):**
   - Matrix Visual hoặc Sankey Diagram: Thể hiện lượng khách du lịch theo cặp Quốc gia Đích vs Quốc gia Nguồn.
