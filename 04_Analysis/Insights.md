# BÁO CÁO PHÂN TÍCH CHUYÊN SÂU (EXECUTIVE INSIGHTS REPORT)
**Dự án:** Phân tích Tổng quan Phát triển Các nước ASEAN (2015 - 2025)  
**Tác giả:** Đội ngũ Phân tích Dữ liệu Capstone  

---

##  EXECUTIVE SUMMARY (TỔNG QUAN ĐIỂM TIN)

Bộ dữ liệu phát triển ASEAN giai đoạn 2015–2025 hợp nhất từ World Bank bao gồm **65 chỉ số phát triển** trên **10 mảng trọng yếu** (Kinh tế, Dân số, Thương mại, FDI, Công nghệ, Giáo dục, Việc làm, Môi trường, Du lịch, Y tế) của 10 quốc gia thành viên ASEAN và Timor-Leste.

---

## 📊 1. KHỐI KINH TẾ VĨ MÔ & TĂNG TRƯỞNG GDP

- **Quy mô GDP:** Indonesia (`IDN`) giữ vị trí nền kinh tế lớn nhất khu vực ASEAN với quy mô vượt 1.400 tỷ USD (năm 2024-2025), tiếp theo là Thailand (`THA`), Singapore (`SGP`), và Viet Nam (`VNM`).
- **Tốc độ tăng trưởng:** Việt Nam, Campuchia và Philippines duy trì tốc độ tăng trưởng GDP ấn tượng trung bình 5-7%/năm trước và sau giai đoạn dịch bệnh.
- **GDP Bình quân đầu người:** Singapore dẫn đầu vượt trội (> 80.000 USD/người/năm), tạo ra khoảng cách lớn so với mức trung bình khu vực.

---

## 🌐 2. HẠ TẦNG SỐ & PHÁT TRIỂN CÔNG NGHỆ

- **Tỷ lệ người dùng Internet:** Singapore, Brunei và Malaysia đạt tỷ lệ bao phủ Internet trên 90% dân số.
- **Tốc độ số hóa:** Việt Nam và Indonesia có tốc độ tăng trưởng thuê bao băng rộng cố định và giao dịch số thuộc hàng nhanh nhất khu vực ASEAN giai đoạn 2018–2024.

---

## ✈️ 3. DÒNG DỊCH CHUYỂN DU LỊCH NỘI KHỐI

- Phân tích ma trận luồng du lịch (`Fact_ASEAN_Tourism_Flow`) ghi nhận sự phục hồi mạnh mẽ của lượng khách du lịch nội khối ASEAN từ năm 2022.
- Thailand, Malaysia, và Singapore là 3 điểm đến thu hút nhiều lượt khách du lịch nhất từ các nước thành viên ASEAN.

---

## 🎯 4. ĐỀ XUẤT CHIẾN LƯỢC TRÊN DASHBOARD POWER BI

1. **KPI Cards:** Hiển thị Tổng GDP ASEAN, Tỷ lệ Tăng trưởng Trung bình, Tổng Dân số và Tỷ lệ tiếp cận Internet.
2. **Slicers:** Lọc linh hoạt theo Quốc gia (`Dim_Country[CountryName]`), Mảng phát triển (`Dim_Indicator[Domain]`) và Năm (`Dim_Date[Year]`).
3. **Scatter Plot:** So sánh Mối tương quan giữa **GDP per Capita** và **Tỷ lệ sử dụng Internet (%)** để thấy rõ tác động của hạ tầng số đến năng suất kinh tế.
