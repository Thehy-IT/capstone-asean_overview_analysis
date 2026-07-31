# 📊 BÁO CÁO CHI TIẾT DANH MỤC INDICATOR THEO 10 NHÓM DATASET (ASEAN 2015 - 2025)

**Dự án:** ASEAN Socio-Economic Development Analysis (2015 - 2025)  
**Nguồn dữ liệu:** World Bank World Development Indicators (WDI) & ASEAN Tourism Statistics  
**Kiến trúc:** 3-Tier Star Schema Model (`Dim_Indicator`, `Fact_ASEAN_Indicators`, `Fact_ASEAN_Tourism_Flow`)  
**Tổng số chỉ số (Indicators):** 65 chỉ số được chuẩn hóa và phân loại vào 10 mảng phát triển kinh tế - xã hội trọng yếu.

---

## 📌 THỐNG KÊ TỔNG QUAN PHÂN BỔ INDICATOR

| STT | Tên Nhóm Phát Triển (Domain) | Số Lượng Chỉ Số | Đơn Vị Tính Phổ Biến | Mô Tả Trọng Tâm Phân Tích |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Kinh tế & GDP** | 7 | `USD`, `% GDP`, `% annual` | Quy mô GDP, tăng trưởng, lạm phát, tích lũy vốn, nợ công & tiết kiệm. |
| 2 | **Dân số & Nhân khẩu học** | 13 | `Person`, `% total`, `births/woman` | Quy mô dân số, tỷ lệ giới tính, đô thị hóa, tỷ lệ sinh & tỷ lệ phụ thuộc. |
| 3 | **Thương mại & Xuất nhập khẩu** | 6 | `USD`, `% GDP` | Xuất nhập khẩu hàng hóa/dịch vụ, kim ngạch thương mại & độ mở kinh tế. |
| 4 | **Đầu tư trực tiếp nước ngoài (FDI)** | 3 | `USD`, `% GDP` | Dòng vốn FDI ròng vào (inflows), ròng ra (outflows) và tỷ trọng FDI/GDP. |
| 5 | **Công nghệ & Hạ tầng số** | 4 | `% population`, `per 100/1M people` | Tỷ lệ dùng Internet, di động, băng rộng cố định & máy chủ bảo mật. |
| 6 | **Giáo dục & Đào tạo** | 11 | `% gross`, `% population`, `% GDP` | Tỷ lệ biết chữ, tỷ lệ nhập học 3 cấp học (Nam/Nữ) & ngân sách giáo dục. |
| 7 | **Lao động & Việc làm** | 6 | `% labor force`, `% employment` | Tỷ lệ tham gia lao động, thất nghiệp (chung/thanh niên) & cơ cấu ngành. |
| 8 | **Môi trường & Năng lượng** | 5 | `% population`, `% land`, `kg oil/capita` | Tiếp cận điện, năng lượng tái tạo, diện tích rừng, tiêu thụ năng lượng & phát thải. |
| 9 | **Du lịch & Dịch vụ** | 1 (+ Bảng Luồng) | `Lượt khách (Person)` | Lượt khách quốc tế nội khối ASEAN & Ma trận di chuyển di dân/du lịch 11 nước. |
| 10 | **Y tế & Sức khỏe** | 9 | `years`, `% GDP`, `per 1,000/100,000` | Tuổi thọ trung bình, chi tiêu y tế, tỷ lệ tử vong trẻ em/người mẹ, y bác sĩ & giường bệnh. |
| **TỔNG** | **10 Nhóm Dataset** | **65 Chỉ Số** | - | **Bộ dữ liệu đa chiều đầy đủ nhất cho phân tích khối ASEAN** |

---

## 📈 1. NHÓM KINH TẾ & GDP (ECONOMY & GDP) - 7 CHỈ SỐ

| STT | Mã Chỉ Số (SeriesCode) | Tên Chỉ Số Gốc (World Bank Series Name) | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `NY.GDP.MKTP.CD` | GDP (current US$) | Tổng sản phẩm quốc nội theo giá hiện hành (USD) | `current US$` |
| 2 | `NY.GDP.MKTP.KD.ZG` | GDP growth (annual %) | Tốc độ tăng trưởng GDP thực tế hàng năm (%) | `annual %` |
| 3 | `NY.GDP.PCAP.CD` | GDP per capita (current US$) | GDP bình quân đầu người theo giá hiện hành (USD/người) | `current US$` |
| 4 | `FP.CPI.TOTL.ZG` | Inflation, consumer prices (annual %) | Tỷ lệ lạm phát dựa trên chỉ số giá tiêu dùng CPI (%) | `annual %` |
| 5 | `GC.DOD.TOTL.GD.ZS` | Central government debt, total (% of GDP) | Tổng dư nợ chính phủ trung ương so với GDP (%) | `% of GDP` |
| 6 | `NE.GDI.TOTL.ZS` | Gross capital formation (% of GDP) | Tích lũy tài sản thô (Đầu tư toàn xã hội) so với GDP (%) | `% of GDP` |
| 7 | `NY.GNS.ICTR.ZS` | Gross savings (% of GDP) | Tổng tiết kiệm quốc dân thô so với GDP (%) | `% of GDP` |

---

## 👥 2. NHÓM DÂN SỐ & NHÂN KHẨU HỌC (POPULATION & DEMOGRAPHICS) - 13 CHỈ SỐ

| STT | Mã Chỉ Số (SeriesCode) | Tên Chỉ Số Gốc (World Bank Series Name) | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `SP.POP.TOTL` | Population, total | Tổng quy mô dân số của quốc gia | `Absolute Unit` (Người) |
| 2 | `SP.POP.GROW` | Population growth (annual %) | Tốc độ tăng trưởng dân số hàng năm (%) | `annual %` |
| 3 | `SP.POP.TOTL.FE.IN` | Population, female | Tổng số lượng dân số Nữ | `Absolute Unit` (Người) |
| 4 | `SP.POP.TOTL.FE.ZS` | Population, female (% of total population) | Tỷ lệ dân số Nữ so với tổng dân số (%) | `% of total population` |
| 5 | `SP.POP.TOTL.MA.IN` | Population, male | Tổng số lượng dân số Nam | `Absolute Unit` (Người) |
| 6 | `SP.POP.TOTL.MA.ZS` | Population, male (% of total population) | Tỷ lệ dân số Nam so với tổng dân số (%) | `% of total population` |
| 7 | `SP.URB.TOTL.IN.ZS` | Urban population (% of total population) | Tỷ lệ dân số sống ở khu vực đô thị (%) | `% of total population` |
| 8 | `SP.DYN.TFRT.IN` | Fertility rate, total (births per woman) | Tỷ lệ sinh tổng số (Số trẻ em bình quân / 1 phụ nữ) | `births per woman` |
| 9 | `SP.POP.0014.TO.ZS` | Population ages 0-14 (% of total population) | Tỷ lệ dân số trẻ em từ 0-14 tuổi (%) | `% of total population` |
| 10 | `SP.POP.65UP.TO.ZS` | Population ages 65 and above (% of total population) | Tỷ lệ dân số người cao tuổi từ 65 tuổi trở lên (%) | `% of total population` |
| 11 | `SP.POP.DPND` | Age dependency ratio (% of working-age population) | Tỷ lệ phụ thuộc tuổi tổng số (% dân số độ tuổi lao động 15-64) | `% of working-age population` |
| 12 | `SP.POP.DPND.OL` | Age dependency ratio, old (% of working-age population) | Tỷ lệ phụ thuộc tuổi già (% dân số độ tuổi lao động) | `% of working-age population` |
| 13 | `SP.POP.DPND.YG` | Age dependency ratio, trẻ em (% of working-age population) | Tỷ lệ phụ thuộc trẻ em (% dân số độ tuổi lao động) | `% of working-age population` |

---

## 🚢 3. NHÓM THƯƠNG MẠI & XUẤT NHẬP KHẨU (TRADE & COMMERCE) - 6 CHỈ SỐ

| STT | Mã Chỉ Số (SeriesCode) | Tên Chỉ Số Gốc (World Bank Series Name) | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `NE.EXP.GNFS.CD` | Exports of goods and services (current US$) | Tổng kim ngạch xuất khẩu hàng hóa và dịch vụ (USD hiện giá) | `current US$` |
| 2 | `NE.IMP.GNFS.CD` | Imports of goods and services (current US$) | Tổng kim ngạch nhập khẩu hàng hóa và dịch vụ (USD hiện giá) | `current US$` |
| 3 | `TX.VAL.MRCH.CD.WT` | Merchandise exports (current US$) | Giá trị xuất khẩu hàng hóa thương mại (USD hiện giá) | `current US$` |
| 4 | `TM.VAL.MRCH.CD.WT` | Merchandise imports (current US$) | Giá trị nhập khẩu hàng hóa thương mại (USD hiện giá) | `current US$` |
| 5 | `TG.VAL.TOTL.GD.ZS` | Merchandise trade (% of GDP) | Kim ngạch thương mại hàng hóa so với GDP (%) | `% of GDP` |
| 6 | `NE.TRD.GNFS.ZS` | Trade (% of GDP) | Tổng kim ngạch xuất nhập khẩu so với GDP (Độ mở nền kinh tế) | `% of GDP` |

---

## 💰 4. NHÓM ĐẦU TƯ TRỰC TIẾP NƯỚC NGOÀI (FDI) - 3 CHỈ SỐ

| STT | Mã Chỉ Số (SeriesCode) | Tên Chỉ Số Gốc (World Bank Series Name) | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `BX.KLT.DINV.CD.WD` | Foreign direct investment, net inflows (BoP, current US$) | Dòng vốn đầu tư trực tiếp nước ngoài (FDI) ròng vào (USD) | `BoP, current US$` |
| 2 | `BM.KLT.DINV.CD.WD` | Foreign direct investment, net outflows (BoP, current US$) | Dòng vốn FDI ròng đầu tư ra nước ngoài (USD) | `BoP, current US$` |
| 3 | `BX.KLT.DINV.WD.GD.ZS` | Foreign direct investment, net inflows (% of GDP) | Tỷ trọng dòng vốn FDI ròng vào so với GDP (%) | `% of GDP` |

---

## 🌐 5. NHÓM CÔNG NGHỆ & HẠ TẦNG SỐ (DIGITAL INFRASTRUCTURE) - 4 CHỈ SỐ

| STT | Mã Chỉ Số (SeriesCode) | Tên Chỉ Số Gốc (World Bank Series Name) | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `IT.NET.USER.ZS` | Individuals using the Internet (% of population) | Tỷ lệ người dân sử dụng Internet trên tổng dân số (%) | `% of population` |
| 2 | `IT.CEL.SETS.P2` | Mobile cellular subscriptions (per 100 people) | Mật độ thuê bao di động (Số hợp đồng / 100 người) | `per 100 people` |
| 3 | `IT.NET.BBND.P2` | Fixed broadband subscriptions (per 100 people) | Thuê bao Internet băng rộng cố định (Số kết nối / 100 người) | `per 100 people` |
| 4 | `IT.NET.SECR.P6` | Secure Internet servers (per 1 million people) | Số lượng máy chủ Internet bảo mật (trên 1 triệu dân) | `per 1 million people` |

---

## 🎓 6. NHÓM GIÁO DỤC & ĐÀO TẠO (EDUCATION & TRAINING) - 11 CHỈ SỐ

| STT | Mã Chỉ Số (SeriesCode) | Tên Chỉ Số Gốc (World Bank Series Name) | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `SE.ADT.LITR.ZS` | Literacy rate, adult total (% of people ages 15+) | Tỷ lệ biết chữ ở người trưởng thành từ 15 tuổi trở lên (%) | `% of people ages 15 and above` |
| 2 | `SE.PRM.ENRR` | School enrollment, primary (% gross) | Tỷ lệ nhập học cấp Tiểu học tổng thể (% gross) | `% gross` |
| 3 | `SE.PRM.ENRR.FE` | School enrollment, primary, female (% gross) | Tỷ lệ nhập học cấp Tiểu học - Học sinh Nữ (% gross) | `% gross` |
| 4 | `SE.PRM.ENRR.MA` | School enrollment, primary, male (% gross) | Tỷ lệ nhập học cấp Tiểu học - Học sinh Nam (% gross) | `% gross` |
| 5 | `SE.SEC.ENRR` | School enrollment, secondary (% gross) | Tỷ lệ nhập học cấp Trung học tổng thể (% gross) | `% gross` |
| 6 | `SE.SEC.ENRR.FE` | School enrollment, secondary, female (% gross) | Tỷ lệ nhập học cấp Trung học - Học sinh Nữ (% gross) | `% gross` |
| 7 | `SE.SEC.ENRR.MA` | School enrollment, secondary, male (% gross) | Tỷ lệ nhập học cấp Trung học - Học sinh Nam (% gross) | `% gross` |
| 8 | `SE.TER.ENRR` | School enrollment, tertiary (% gross) | Tỷ lệ nhập học cấp Cao đẳng / Đại học tổng thể (% gross) | `% gross` |
| 9 | `SE.TER.ENRR.FE` | School enrollment, tertiary, female (% gross) | Tỷ lệ nhập học cấp Cao đẳng / Đại học - Nữ (% gross) | `% gross` |
| 10 | `SE.TER.ENRR.MA` | School enrollment, tertiary, male (% gross) | Tỷ lệ nhập học cấp Cao đẳng / Đại học - Nam (% gross) | `% gross` |
| 11 | `SE.XPD.TOTL.GD.ZS` | Government expenditure on education, total (% of GDP) | Chi tiêu ngân sách nhà nước cho giáo dục so với GDP (%) | `% of GDP` |

---

## 💼 7. NHÓM LAO ĐỘNG & VIỆC LÀM (LABOR FORCE & EMPLOYMENT) - 6 CHỈ SỐ

| STT | Mã Chỉ Số (SeriesCode) | Tên Chỉ Số Gốc (World Bank Series Name) | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `SL.TLF.CACT.ZS` | Labor force participation rate, total (% 15+) | Tỷ lệ tham gia lực lượng lao động (dân số 15+ tuổi, ước tính ILO) | `% of total population ages 15+` |
| 2 | `SL.UEM.TOTL.ZS` | Unemployment, total (% of total labor force) | Tỷ lệ thất nghiệp tổng thể (% lực lượng lao động, ước tính ILO) | `% of total labor force` |
| 3 | `SL.UEM.1524.ZS` | Unemployment, youth total (% 15-24) | Tỷ lệ thất nghiệp trong độ tuổi thanh niên 15-24 tuổi (%) | `% of total labor force ages 15-24` |
| 4 | `SL.AGR.EMPL.ZS` | Employment in agriculture (% of total employment) | Tỷ lệ lao động làm việc trong ngành Nông nghiệp (%) | `% of total employment` |
| 5 | `SL.IND.EMPL.ZS` | Employment in industry (% of total employment) | Tỷ lệ lao động làm việc trong ngành Công nghiệp (%) | `% of total employment` |
| 6 | `SL.SRV.EMPL.ZS` | Employment in services (% of total employment) | Tỷ lệ lao động làm việc trong ngành Dịch vụ (%) | `% of total employment` |

---

## 🍃 8. NHÓM MÔI TRƯỜNG & NĂNG LƯỢNG (ENVIRONMENT & ENERGY) - 5 CHỈ SỐ

| STT | Mã Chỉ Số (SeriesCode) | Tên Chỉ Số Gốc (World Bank Series Name) | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `EG.ELC.ACCS.ZS` | Access to electricity (% of population) | Tỷ lệ dân số được tiếp cận và sử dụng điện lưới (%) | `% of population` |
| 2 | `EG.FEC.RNEW.ZS` | Renewable energy consumption (% of final energy) | Tỷ lệ tiêu thụ năng lượng tái tạo trong tổng tiêu thụ năng lượng (%) | `% of total final energy consumption` |
| 3 | `EG.USE.PCAP.KG.OE` | Energy use (kg of oil equivalent per capita) | Mức tiêu thụ năng lượng bình quân đầu người (kg tương đương dầu) | `kg of oil equivalent per capita` |
| 4 | `AG.LND.FRST.ZS` | Forest area (% of land area) | Tỷ lệ diện tích đất có rừng che phủ so với tổng diện tích đất (%) | `% of land area` |
| 5 | `NY.ADJ.DCO2.GN.ZS` | Adjusted savings: carbon dioxide damage (% GNI) | Chi phí tổn thất do phát thải CO2 tính theo phần trăm GNI (%) | `% of GNI` |

---

## ✈️ 9. NHÓM DU LỊCH & DỊCH VỤ (TOURISM & SERVICES) - 1 CHỈ SỐ CHÍNH + FACT MATRIX

| STT | Mã Chỉ Số / Bảng dữ liệu | Tên Gốc / Tên Bảng | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `ST.INT.ARVL.TOTL` | International tourism, number of arrivals | Tổng số lượt khách du lịch quốc tế nhập cảnh từ các nước ASEAN | `Lượt khách (Person)` |
| 2 | `Fact_ASEAN_Tourism_Flow` *(Bảng Fact Luồng)* | ASEAN Intra-Regional Tourism Matrix (917 records) | Ma trận di chuyển du lịch giữa 11 quốc gia Nguồn (Origin) & Đích (Destination) | `Lượt khách (Person)` |

---

## 🏥 10. NHÓM Y TẾ & SỨC KHỎE (HEALTH & WELLBEING) - 9 CHỈ SỐ

| STT | Mã Chỉ Số (SeriesCode) | Tên Chỉ Số Gốc (World Bank Series Name) | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `SP.DYN.LE00.IN` | Life expectancy at birth, total (years) | Tuổi thọ trung bình dự kiến khi sinh (Số năm) | `years` |
| 2 | `SH.XPD.CHEX.GD.ZS` | Current health expenditure (% of GDP) | Tổng chi tiêu cho y tế hiện tại so với GDP (%) | `% of GDP` |
| 3 | `SH.DYN.MORT` | Mortality rate, under-5 (per 1,000 live births) | Tỷ lệ tử vong ở trẻ em dưới 5 tuổi (trên 1.000 trẻ sinh sống) | `per 1,000 live births` |
| 4 | `SH.DYN.MORT.FE` | Mortality rate, under-5, female (per 1,000) | Tỷ lệ tử vong ở trẻ Nữ dưới 5 tuổi (trên 1.000 trẻ sinh sống) | `per 1,000 live births` |
| 5 | `SH.DYN.MORT.MA` | Mortality rate, under-5, male (per 1,000) | Tỷ lệ tử vong ở trẻ Nam dưới 5 tuổi (trên 1.000 trẻ sinh sống) | `per 1,000 live births` |
| 6 | `SH.STA.MMRT` | Maternal mortality ratio (modeled estimate) | Tỷ lệ tử vong ở sản phụ khi sinh (Ước tính mô hình / 100.000 trẻ sinh) | `modeled estimate, per 100,000 live births` |
| 7 | `SH.STA.MMRT.NE` | Maternal mortality ratio (national estimate) | Tỷ lệ tử vong ở sản phụ khi sinh (Báo cáo quốc gia / 100.000 trẻ sinh) | `national estimate, per 100,000 live births` |
| 8 | `SH.MED.BEDS.ZS` | Hospital beds (per 1,000 people) | Mật độ giường bệnh viện (Số giường / 1.000 người dân) | `per 1,000 people` |
| 9 | `SH.MED.PHYS.ZS` | Physicians (per 1,000 people) | Mật độ bác sĩ y khoa (Số bác sĩ / 1.000 người dân) | `per 1,000 people` |

---

## 🛠️ HƯỚNG DẪN TRUY VẤN VÀ KHÁM PHÁ TRÊN POWER BI / SQL

- **Bảng Chiều Chỉ Số (`Dim_Indicator`):** Dùng làm Slicer / Filter theo trường `Domain` để chọn 1 trong 10 nhóm trên.
- **Bảng Sự Kiện (`Fact_ASEAN_Indicators`):** Liên kết `Dim_Indicator[SeriesCode] = Fact_ASEAN_Indicators[SeriesCode]` (Quan hệ 1:N).
- **DAX Measure Mẫu:**
  ```dax
  Average Indicator Value = 
  CALCULATE(
      AVERAGE(Fact_ASEAN_Indicators[Value]),
      USERELATIONSHIP(Dim_Date[Year], Fact_ASEAN_Indicators[Year])
  )
  ```
