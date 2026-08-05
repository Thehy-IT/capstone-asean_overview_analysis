# BÁO CÁO CHI TIẾT DANH MỤC INDICATOR THEO 10 NHÓM DATASET (ASEAN 2015 - 2025)

**Dự án:** Phân tích Phát triển Kinh tế - Xã hội ASEAN (2015 - 2025)  
**Nguồn dữ liệu:** World Bank World Development Indicators (WDI) & ASEAN Tourism Statistics  
**Kiến trúc dữ liệu:** Mô hình 3-Tier Star Schema (`Dim_Indicator`, `Fact_ASEAN_Indicators`, `Fact_ASEAN_Tourism_Flow`)  
**Tổng số chỉ số (Indicators):** 65 chỉ số được chuẩn hóa và phân loại vào 10 mảng phát triển kinh tế - xã hội trọng yếu  
**Phiên bản tài liệu:** 2.0 (Báo cáo Kỹ thuật Chính thức)  

---

## I. TỔNG QUAN PHÂN BỔ DANH MỤC CHỈ SỐ

Dưới đây là bảng thống kê tổng hợp phân bổ 65 chỉ số thuộc 10 mảng phát triển kinh tế - xã hội khối ASEAN giai đoạn 2015 – 2025. Bộ dữ liệu được thiết kế nhằm phục vụ bài toán phân tích vĩ mô, đối sánh hiệu quả phát triển giữa các quốc gia thành viên và xây dựng hệ thống báo cáo quản trị trên Power BI / SQL Data Warehouse.

| STT | Nhóm Lĩnh Vực (Domain) | Số Lượng Chỉ Số | Đơn Vị Tính Phổ Biến | Phạm Vi & Mục Tiêu Phân Tích |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Kinh tế & GDP** | 7 | `USD`, `% GDP`, `% annual` | Quy mô GDP, tốc độ tăng trưởng, lạm phát, tích lũy tài sản, nợ công và tỷ lệ tiết kiệm quốc dân. |
| 2 | **Dân số & Nhân khẩu học** | 13 | `Person`, `% total`, `births/woman` | Quy mô dân số, cơ cấu giới tính, đô thị hóa, tỷ lệ sinh và tỷ lệ phụ thuộc tuổi. |
| 3 | **Thương mại & Xuất nhập khẩu** | 6 | `USD`, `% GDP` | Kim ngạch xuất nhập khẩu hàng hóa/dịch vụ, kim ngạch thương mại và độ mở kinh tế. |
| 4 | **Đầu tư trực tiếp nước ngoài (FDI)** | 3 | `USD`, `% GDP` | Dòng vốn FDI ròng vào (inflows), ròng ra (outflows) và tỷ trọng FDI so với GDP. |
| 5 | **Công nghệ & Hạ tầng số** | 4 | `% population`, `per 100/1M people` | Tỷ lệ phổ cập Internet, mật độ di động, kết nối băng rộng cố định và hạ tầng máy chủ an toàn. |
| 6 | **Giáo dục & Đào tạo** | 11 | `% gross`, `% population`, `% GDP` | Tỷ lệ biết chữ, tỷ lệ nhập học 3 cấp (Tiểu học, Trung học, Đại học) phân tách theo giới và ngân sách giáo dục. |
| 7 | **Lao động & Việc làm** | 6 | `% labor force`, `% employment` | Tỷ lệ tham gia lực lượng lao động, thất nghiệp (chung và thanh niên) và cơ cấu việc làm 3 ngành. |
| 8 | **Môi trường & Năng lượng** | 5 | `% population`, `% land`, `kg oil/capita` | Tiếp cận điện lưới, năng lượng tái tạo, tiêu thụ năng lượng bình quân, tỷ lệ che phủ rừng và tổn thất CO2. |
| 9 | **Du lịch & Dịch vụ** | 1 (+ Fact Luồng) | `Lượt khách (Person)` | Tổng lượt khách du lịch quốc tế và Ma trận luồng khách di chuyển nội khối 11 quốc gia. |
| 10 | **Y tế & Sức khỏe** | 9 | `years`, `% GDP`, `per 1,000/100,000` | Tuổi thọ trung bình, chi tiêu y tế/GDP, tỷ lệ tử vong trẻ em/sản phụ, mật độ bác sĩ và giường bệnh. |
| **TỔNG** | **10 Nhóm Lĩnh Vực** | **65 Chỉ Số** | - | **Hệ thống chỉ số toàn diện phục vụ phân tích đa chiều khối ASEAN** |

---

## II. CHI TIẾT DANH MỤC 65 CHỈ SỐ THEO 10 NHÓM DATASET

### 1. Nhóm Kinh tế & GDP (Economy & GDP) — 7 Chỉ số

Tập dữ liệu theo dõi sức khỏe kinh tế vĩ mô, quy mô sản lượng và tính ổn định tài chính quốc gia.

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

### 2. Nhóm Dân số & Nhân khẩu học (Population & Demographics) — 13 Chỉ số

Tập dữ liệu cung cấp bức tranh về quy mô dân số, biến động nhân khẩu, mức độ đô thị hóa và áp lực phụ thuộc tuổi.

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
| 11 | `SP.POP.DPND` | Age dependency ratio (% of working-age population) | Tỷ lệ phụ thuộc tuổi tổng số (% dân số độ tuổi 15-64) | `% of working-age population` |
| 12 | `SP.POP.DPND.OL` | Age dependency ratio, old (% of working-age population) | Tỷ lệ phụ thuộc tuổi già (% dân số độ tuổi lao động) | `% of working-age population` |
| 13 | `SP.POP.DPND.YG` | Age dependency ratio, young (% of working-age population) | Tỷ lệ phụ thuộc trẻ em (% dân số độ tuổi lao động) | `% of working-age population` |

---

### 3. Nhóm Thương mại & Xuất nhập khẩu (Trade & Commerce) — 6 Chỉ số

Tập dữ liệu phản ánh mức độ hội nhập thương mại quốc tế, quy mô xuất nhập khẩu và độ mở kinh tế.

| STT | Mã Chỉ Số (SeriesCode) | Tên Chỉ Số Gốc (World Bank Series Name) | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `NE.EXP.GNFS.CD` | Exports of goods and services (current US$) | Tổng kim ngạch xuất khẩu hàng hóa và dịch vụ (USD hiện giá) | `current US$` |
| 2 | `NE.IMP.GNFS.CD` | Imports of goods and services (current US$) | Tổng kim ngạch nhập khẩu hàng hóa và dịch vụ (USD hiện giá) | `current US$` |
| 3 | `TX.VAL.MRCH.CD.WT` | Merchandise exports (current US$) | Giá trị xuất khẩu hàng hóa thương mại (USD hiện giá) | `current US$` |
| 4 | `TM.VAL.MRCH.CD.WT` | Merchandise imports (current US$) | Giá trị nhập khẩu hàng hóa thương mại (USD hiện giá) | `current US$` |
| 5 | `TG.VAL.TOTL.GD.ZS` | Merchandise trade (% of GDP) | Kim ngạch thương mại hàng hóa so với GDP (%) | `% of GDP` |
| 6 | `NE.TRD.GNFS.ZS` | Trade (% of GDP) | Tổng kim ngạch xuất nhập khẩu so với GDP (Độ mở nền kinh tế) | `% of GDP` |

---

### 4. Nhóm Đầu tư trực tiếp nước ngoài (FDI) — 3 Chỉ số

Tập dữ liệu đo lường mức độ thu hút nguồn vốn quốc tế và xu hướng đầu tư ra nước ngoài của các quốc gia ASEAN.

| STT | Mã Chỉ Số (SeriesCode) | Tên Chỉ Số Gốc (World Bank Series Name) | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `BX.KLT.DINV.CD.WD` | Foreign direct investment, net inflows (BoP, current US$) | Dòng vốn đầu tư trực tiếp nước ngoài (FDI) ròng vào (USD) | `BoP, current US$` |
| 2 | `BM.KLT.DINV.CD.WD` | Foreign direct investment, net outflows (BoP, current US$) | Dòng vốn FDI ròng đầu tư ra nước ngoài (USD) | `BoP, current US$` |
| 3 | `BX.KLT.DINV.WD.GD.ZS` | Foreign direct investment, net inflows (% of GDP) | Tỷ trọng dòng vốn FDI ròng vào so với GDP (%) | `% of GDP` |

---

### 5. Nhóm Công nghệ & Hạ tầng số (Digital Infrastructure) — 4 Chỉ số

Tập dữ liệu đánh giá năng lực sẵn sàng chuyển đổi số, hạ tầng viễn thông và mức độ an toàn thông tin.

| STT | Mã Chỉ Số (SeriesCode) | Tên Chỉ Số Gốc (World Bank Series Name) | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `IT.NET.USER.ZS` | Individuals using the Internet (% of population) | Tỷ lệ người dân sử dụng Internet trên tổng dân số (%) | `% of population` |
| 2 | `IT.CEL.SETS.P2` | Mobile cellular subscriptions (per 100 people) | Mật độ thuê bao di động (Số hợp đồng / 100 người) | `per 100 people` |
| 3 | `IT.NET.BBND.P2` | Fixed broadband subscriptions (per 100 people) | Thuê bao Internet băng rộng cố định (Số kết nối / 100 người) | `per 100 people` |
| 4 | `IT.NET.SECR.P6` | Secure Internet servers (per 1 million people) | Số lượng máy chủ Internet bảo mật (trên 1 triệu dân) | `per 1 million people` |

---

### 6. Nhóm Giáo dục & Đào tạo (Education & Training) — 11 Chỉ số

Tập dữ liệu phản ánh chất lượng nguồn nhân lực, bình đẳng giới trong giáo dục và mức độ đầu tư ngân sách cho giáo dục.

| STT | Mã Chỉ Số (SeriesCode) | Tên Chỉ Số Gốc (World Bank Series Name) | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `SE.ADT.LITR.ZS` | Literacy rate, adult total (% of people ages 15+) | Tỷ lệ biết chữ ở người trưởng thành từ 15 tuổi trở lên (%) | `% of people ages 15+` |
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

### 7. Nhóm Lao động & Việc làm (Labor Force & Employment) — 6 Chỉ số

Tập dữ liệu phân tích mức độ tham gia thị trường lao động, tỷ lệ thất nghiệp và sự dịch chuyển cơ cấu kinh tế theo ngành.

| STT | Mã Chỉ Số (SeriesCode) | Tên Chỉ Số Gốc (World Bank Series Name) | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `SL.TLF.CACT.ZS` | Labor force participation rate, total (% 15+) | Tỷ lệ tham gia lực lượng lao động (dân số 15+ tuổi, ước tính ILO) | `% of total population 15+` |
| 2 | `SL.UEM.TOTL.ZS` | Unemployment, total (% of total labor force) | Tỷ lệ thất nghiệp tổng thể (% lực lượng lao động, ước tính ILO) | `% of total labor force` |
| 3 | `SL.UEM.1524.ZS` | Unemployment, youth total (% 15-24) | Tỷ lệ thất nghiệp trong độ tuổi thanh niên 15-24 tuổi (%) | `% of labor force 15-24` |
| 4 | `SL.AGR.EMPL.ZS` | Employment in agriculture (% of total employment) | Tỷ lệ lao động làm việc trong ngành Nông nghiệp (%) | `% of total employment` |
| 5 | `SL.IND.EMPL.ZS` | Employment in industry (% of total employment) | Tỷ lệ lao động làm việc trong ngành Công nghiệp (%) | `% of total employment` |
| 6 | `SL.SRV.EMPL.ZS` | Employment in services (% of total employment) | Tỷ lệ lao động làm việc trong ngành Dịch vụ (%) | `% of total employment` |

---

### 8. Nhóm Môi trường & Năng lượng (Environment & Energy) — 5 Chỉ số

Tập dữ liệu phục vụ phân tích phát triển bền vững, an ninh năng lượng và tác động môi trường trong quá trình tăng trưởng.

| STT | Mã Chỉ Số (SeriesCode) | Tên Chỉ Số Gốc (World Bank Series Name) | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `EG.ELC.ACCS.ZS` | Access to electricity (% of population) | Tỷ lệ dân số được tiếp cận và sử dụng điện lưới (%) | `% of population` |
| 2 | `EG.FEC.RNEW.ZS` | Renewable energy consumption (% of final energy) | Tỷ lệ tiêu thụ năng lượng tái tạo trong tổng tiêu thụ năng lượng (%) | `% of total final energy` |
| 3 | `EG.USE.PCAP.KG.OE` | Energy use (kg of oil equivalent per capita) | Mức tiêu thụ năng lượng bình quân đầu người (kg tương đương dầu) | `kg oil equivalent/capita` |
| 4 | `AG.LND.FRST.ZS` | Forest area (% of land area) | Tỷ lệ diện tích đất có rừng che phủ so với tổng diện tích đất (%) | `% of land area` |
| 5 | `NY.ADJ.DCO2.GN.ZS` | Adjusted savings: carbon dioxide damage (% GNI) | Chi phí tổn thất do phát thải CO2 tính theo phần trăm GNI (%) | `% of GNI` |

---

### 9. Nhóm Du lịch & Dịch vụ (Tourism & Services) — 1 Chỉ số chính + Fact Luồng

Tập dữ liệu phản ánh liên kết giao lưu nội khối và quy mô thu hút du khách giữa 11 quốc gia Đông Nam Á.

| STT | Mã Chỉ Số / Bảng dữ liệu | Tên Gốc / Tên Bảng | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `ST.INT.ARVL.TOTL` | International tourism, number of arrivals | Tổng số lượt khách du lịch quốc tế nhập cảnh từ các nước ASEAN | `Lượt khách (Person)` |
| 2 | `Fact_ASEAN_Tourism_Flow` *(Bảng Fact Luồng)* | ASEAN Intra-Regional Tourism Matrix (908 records) | Ma trận di chuyển du lịch hai chiều giữa 11 quốc gia Nguồn (Origin) & Đích (Destination) | `Lượt khách (Person)` |

---

### 10. Nhóm Y tế & Sức khỏe (Health & Wellbeing) — 9 Chỉ số

Tập dữ liệu đánh giá an sinh xã hội, chất lượng chăm sóc sức khỏe cộng đồng và năng lực hạ tầng y tế.

| STT | Mã Chỉ Số (SeriesCode) | Tên Chỉ Số Gốc (World Bank Series Name) | Tên Tiếng Việt & Diễn Giải | Đơn Vị Tính (UnitOfMeasure) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `SP.DYN.LE00.IN` | Life expectancy at birth, total (years) | Tuổi thọ trung bình dự kiến khi sinh (Số năm) | `years` |
| 2 | `SH.XPD.CHEX.GD.ZS` | Current health expenditure (% of GDP) | Tổng chi tiêu cho y tế hiện tại so với GDP (%) | `% of GDP` |
| 3 | `SH.DYN.MORT` | Mortality rate, under-5 (per 1,000 live births) | Tỷ lệ tử vong ở trẻ em dưới 5 tuổi (trên 1.000 trẻ sinh sống) | `per 1,000 live births` |
| 4 | `SH.DYN.MORT.FE` | Mortality rate, under-5, female (per 1,000) | Tỷ lệ tử vong ở trẻ Nữ dưới 5 tuổi (trên 1.000 trẻ sinh sống) | `per 1,000 live births` |
| 5 | `SH.DYN.MORT.MA` | Mortality rate, under-5, male (per 1,000) | Tỷ lệ tử vong ở trẻ Nam dưới 5 tuổi (trên 1.000 trẻ sinh sống) | `per 1,000 live births` |
| 6 | `SH.STA.MMRT` | Maternal mortality ratio (modeled estimate) | Tỷ lệ tử vong sản phụ khi sinh (Ước tính mô hình / 100.000 trẻ sinh) | `per 100,000 live births` |
| 7 | `SH.STA.MMRT.NE` | Maternal mortality ratio (national estimate) | Tỷ lệ tử vong sản phụ khi sinh (Báo cáo quốc gia / 100.000 trẻ sinh) | `per 100,000 live births` |
| 8 | `SH.MED.BEDS.ZS` | Hospital beds (per 1,000 people) | Mật độ giường bệnh viện (Số giường / 1.000 người dân) | `per 1,000 people` |
| 9 | `SH.MED.PHYS.ZS` | Physicians (per 1,000 people) | Mật độ bác sĩ y khoa (Số bác sĩ / 1.000 người dân) | `per 1,000 people` |

---

## III. THIẾT KẾ MÔ HÌNH DỮ LIỆU VÀ BẢNG NGUYÊN TẮC QUẢN TRỊ DAX / SQL

### 1. Cấu trúc Mô hình Ngôi sao (Star Schema Architecture)

Toàn bộ 65 chỉ số và ma trận luồng du lịch được tổ chức theo tiêu chuẩn mô hình dữ liệu quan hệ cho Business Intelligence:

- **Bảng Chiều Chỉ Số (`Dim_Indicator`):** Chứa metadata chi tiết cho 65 chỉ số (Mã chỉ số `SeriesCode`, tên chỉ số tiếng Anh/tiếng Việt, nhóm lĩnh vực `Domain`, đơn vị tính `UnitOfMeasure`).
- **Bảng Chiều Quốc Gia (`Dim_Country`):** Chứa thông tin 11 quốc gia ASEAN (Mã ISO3 `CountryCode`, tên tiếng Anh, tên tiếng Việt, khu vực đại lục/hải đảo).
- **Bảng Chiều Thời Gian (`Dim_Date`):** Khóa chính `Year` (2015 – 2025), chuỗi ngày chuẩn hóa hỗ trợ hàm Time-Intelligence trong DAX.
- **Bảng Sự Kiện Chỉ Số (`Fact_ASEAN_Indicators`):** Chứa 6,730 bản ghi dữ liệu đã unpivot theo hạt nhân `(CountryCode, SeriesCode, Year, Value)`.
- **Bảng Sự Kiện Luồng Du Lịch (`Fact_ASEAN_Tourism_Flow`):** Chứa 908 bản ghi luồng du khách với khóa ngoại kép `DestinationCode` và `OriginCode` liên kết tới `Dim_Country`.

### 2. Nguyên tắc Gom nhóm & Hàm Tổng hợp trong DAX

| Nhóm Loại Dữ Liệu | Ví dụ Chỉ số | Hàm Tổng hợp Khuyến nghị | Ghi chú & Rủi ro Kỹ thuật |
| :--- | :--- | :--- | :--- |
| **Giá trị Tuyệt đối (Absolute Quantities)** | GDP (`NY.GDP.MKTP.CD`), Dân số (`SP.POP.TOTL`), FDI (`BX.KLT.DINV.CD.WD`) | `SUM()` theo năm / quốc gia; `AVERAGE()` khi aggregate nhiều năm | Có thể cộng dồn các quốc gia để tính tổng toàn khối ASEAN. |
| **Tỷ lệ Phần trăm so với GDP / GNI** | Nợ công (% GDP), FDI (% GDP), Chi tiêu Giáo dục (% GDP) | `AVERAGE()` hoặc Weighted Average theo GDP | **Không dùng `SUM()`** để tránh tính sai tỷ lệ tổng thể. |
| **Tỷ lệ Phần trăm Dân số / Lao động** | Tỷ lệ dùng Internet (%), Thất nghiệp (%), Đô thị hóa (%) | `AVERAGE()` hoặc Weighted Average theo Dân số / Lực lượng lao động | Phải nhân với quy mô dân số trước khi tính trung bình gia quyền toàn khối. |
| **Mật độ trên Quy mô Dân số** | Thuê bao di động (/100 dân), Giường bệnh (/1.000 dân), Bác sĩ (/1.000 dân) | `AVERAGE()` | Giá trị có thể vượt quá 100 (ví dụ thuê bao di động người dân dùng nhiều SIM). |
| **Chỉ số Luồng Hai chiều (Flow Matrix)** | Luồng du khách (`Fact_ASEAN_Tourism_Flow`) | `SUM(Arrivals)` kết hợp `USERELATIONSHIP()` | Cần áp dụng kỹ thuật **Role-Playing Dimension** trong Power BI khi lọc theo Điểm đi (Origin) hoặc Điểm đến (Destination). |

---

## IV. NGUYÊN TẮC XỬ LÝ DỮ LIỆU KHUYẾT VÀ BẤT THƯỜNG

1. **Ký tự Sentinel:** Toàn bộ ký tự `".."` trong dữ liệu thô World Bank đã được chuyển đổi về `NULL` / `NaN` để đảm bảo tính chính xác của các phép toán số học.
2. **Dữ liệu Dự báo 2025:** Giá trị các chỉ số năm 2025 ở một số mảng là số liệu ước tính/dự báo từ World Bank; cần hiển thị ghi chú thích hợp trên giao diện báo cáo.
3. **Giá trị Âm Hợp lệ:** Các giá trị âm ở chỉ số FDI Ròng (`BX.KLT.DINV.CD.WD`) thể hiện hiện tượng rút vốn thuần (net disinvestment) và được giữ nguyên giá trị thực tế.
4. **Tỷ lệ Nhập học Thô > 100%:** Chỉ số `SE.PRM.ENRR` (Gross Primary Enrollment) có thể vượt 100% do nhập học sớm hoặc muộn so với độ tuổi chuẩn; đây là tính chất dữ liệu hợp lệ của UNESCO/World Bank, không loại bỏ dưới dạng outlier.

---

**Báo cáo được phê duyệt và phát hành bởi:** Bộ phận Phân tích Dữ liệu Dự án ASEAN Overview Analysis  
**Trạng thái kiểm định:** Đã xác minh 100% mã chỉ số và liên kết khóa ngoại mô hình Star Schema.
