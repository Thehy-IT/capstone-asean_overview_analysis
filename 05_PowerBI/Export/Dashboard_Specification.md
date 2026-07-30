# 🎨 POWER BI DASHBOARD UI/UX SPECIFICATION & BLUEPRINT
**Project:** ASEAN Socio-Economic & Development Analysis (2015 - 2025)  
**Author:** Senior BI Solution Architect & UX/UI Designer  

---

## 🖥️ 1. GLOBAL DESIGN SYSTEM & THEME TOKENS

### Color Palette (ASEAN Professional Dark Theme)
- **Primary Canvas Background:** `#0F172A` (Slate Navy 900)
- **Card / Visual Container Background:** `#1E293B` (Slate Navy 800)
- **Container Border:** 1px solid `#334155` (Slate Navy 700) with 8px Border Radius
- **Primary Accent (ASEAN Blue):** `#0284C7` (Sky Blue)
- **Secondary Accent (ASEAN Gold/Yellow):** `#F59E0B` (Amber Gold)
- **Success / Digital Growth:** `#10B981` (Emerald Green)
- **Alert / Inflation Risk:** `#EF4444` (Coral Red)
- **Typography:** Segoe UI / Inter (Headers: Bold 14pt White `#F8FAFC`, Subtitles: Regular 10pt `#94A3B8`)

---

## 📐 2. PAGE-BY-PAGE DASHBOARD WIREFRAME SPECIFICATIONS

```text
+-----------------------------------------------------------------------------------------+
| [HEADER BAR] Logo ASEAN | Title: ASEAN Socio-Economic Analysis | Slicers: [Year] [Country] |
+-----------------------------------------------------------------------------------------+
| [KPI 1: Total GDP]    | [KPI 2: Avg Growth]    | [KPI 3: Total Pop]   | [KPI 4: Internet %] |
| $3.81 Trillion USD    | +3.54% YoY             | 680.5 Million        | 62.49%              |
+-----------------------+------------------------+----------------------+---------------------+
| [VISUAL A: GDP Treemap / Bar Chart]           | [VISUAL B: GDP Growth Line Trend 2015-2025] |
| Tỷ trọng GDP 10 nước ASEAN                    | Diễn biến tăng trưởng GDP qua các năm       |
+-----------------------------------------------+---------------------------------------------+
| [VISUAL C: Internet Penetration Slope Chart]  | [VISUAL D: Top Intra-ASEAN Tourism Flow]    |
| Bước nhảy vọt số hóa 2015 vs 2023             | Hành lang du lịch nội khối sôi động nhất    |
+-----------------------------------------------+---------------------------------------------+
```

---

## 📄 PAGE 1: EXECUTIVE MACROECONOMIC OVERVIEW (TỔNG QUAN KINH TẾ VĨ MÔ)

### Visual Layout & Components:
1. **Header Banner (Top Row):**
   - Title: *"ASEAN Economic Landscape & GDP Growth Dynamics"*
   - Slicers: `Dim_Date[Year]` (Dropdown), `Dim_Country[SubRegion]` (Tile/Buttons).
2. **KPI Summary Cards (4 Cards):**
   - **Card 1 (Total ASEAN GDP):** Measure `[GDP (Current US$)]` $\rightarrow$ Display: `$3.81T USD`.
   - **Card 2 (Average GDP Growth Rate):** Measure `[GDP Growth Rate (%)]` $\rightarrow$ Display: `+3.54%`.
   - **Card 3 (Total Population):** Measure `[Total Population]` $\rightarrow$ Display: `680.5M`.
   - **Card 4 (GDP Share Top 3):** Measure `[GDP Share Top 3]` $\rightarrow$ Display: `62.94%`.
3. **Main Visual A (Treemap - Left Center):**
   - Category: `Dim_Country[CountryName]`
   - Values: `[GDP (Current US$)]`
   - Tooltip: `[GDP YoY %]`, `[GDP Per Capita (US$)]`.
4. **Main Visual B (Combo Line & Clustered Column - Right Center):**
   - Shared Axis: `Dim_Date[Year]`
   - Column Values: `[GDP (Current US$)]`
   - Line Values: `[GDP Growth Rate (%)]`.

---

## 📄 PAGE 2: DIGITAL ECONOMY & HUMAN CAPITAL (CHUYỂN ĐỔI SỐ & NGUỒN NHÂN LỰC)

### Visual Layout & Components:
1. **KPI Cards (Top Row):**
   - **Card 1 (Avg Internet Penetration):** `[Internet Users (% Pop)]` $\rightarrow$ Display: `62.49%`.
   - **Card 2 (Digital Champion Jump):** `Cambodia (+62.49%)`.
2. **Visual A (Clustered Bar Chart - Left):**
   - Y-Axis: `Dim_Country[CountryName]`
   - X-Axis: `[Internet Users (% Pop)]` for Year 2015 vs 2023.
3. **Visual B (Scatter Plot - Right):**
   - X-Axis: `[Internet Users (% Pop)]`
   - Y-Axis: `[GDP Per Capita (US$)]`
   - Size: `[Total Population]`
   - Legend: `Dim_Country[SubRegion]`.

---

## 📄 PAGE 3: INTRA-ASEAN TOURISM FLOW MATRIX (MA TRẬN DU LỊCH NỘI KHỐI)

### Visual Layout & Components:
1. **KPI Cards (Top Row):**
   - **Card 1 (Total Intra-ASEAN Arrivals):** `[Tourism Visitors Total]` $\rightarrow$ Display: `30.7M Visitors`.
   - **Card 2 (Top Tourist Corridor):** `Singapore -> Malaysia (8.31M)`.
2. **Visual A (Matrix Visual - Center Left):**
   - Rows: `Dim_Country[CountryName]` (Destination)
   - Columns: `Fact_ASEAN_Tourism_Flow[OriginCountryCode]` (Origin)
   - Values: `[Tourism Visitors Flow]` (Formatted as integer number with commas).
3. **Visual B (Bar Chart - Center Right):**
   - Top 10 Tourist Origin-Destination Pairs sorted descending by `Visitors`.

---

## 📄 PAGE 4: COUNTRY SCORECARD DEEP-DIVE (BÁO CÁO CHI TIẾT THEO QUỐC GIA)

### Visual Layout & Components:
1. **Dynamic Header:** Measure `[Dynamic Dashboard Title]` (Auto-changes when user clicks a country).
2. **Single Country Selector Slicer:** `Dim_Country[CountryName]`.
3. **Multi-Domain KPI Grid:**
   - GDP & GDP Growth Rate
   - Inflation Rate (%)
   - Population & Labor Force
   - Internet Penetration (%)
   - Total Foreign Direct Investment (FDI)
