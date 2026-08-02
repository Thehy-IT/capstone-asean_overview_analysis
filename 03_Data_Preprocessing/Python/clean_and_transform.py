import os
import sys
import glob
import re
import csv

# Set stdout/stderr encoding to utf-8 for Windows console safety
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Define directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DIR = os.path.join(BASE_DIR, "02_Data", "Raw")
CLEANED_DIR = os.path.join(BASE_DIR, "02_Data", "Cleaned")

os.makedirs(CLEANED_DIR, exist_ok=True)

# Domain mapping for raw CSV files
DOMAIN_MAPPING = {
    "congnghe-Data.csv": "Công nghệ & Hạ tầng số",
    "danso-Data.csv": "Dân số & Nhân khẩu học",
    "dulich-Data.csv": "Du lịch & Dịch vụ",
    "fdi-Data.csv": "Đầu tư trực tiếp nước ngoài (FDI)",
    "giaoduc-Data.csv": "Giáo dục & Đào tạo",
    "kinhte-Data.csv": "Kinh tế & GDP",
    "moitruong-Data.csv": "Môi trường & Năng lượng",
    "thuongmai-Data.csv": "Thương mại & Xuất nhập khẩu",
    "vieclam-Data.csv": "Lao động & Việc làm",
    "yte-Data.csv": "Y tế & Sức khỏe"
}

# ISO2/ISO3 country mapping helper for Tourism & Metadata
COUNTRY_CODE_MAP = {
    "BRN": "BRN", "BN": "BRN", "Brunei Darussalam": "BRN", "Brunei": "BRN",
    "KHM": "KHM", "KH": "KHM", "Cambodia": "KHM",
    "IDN": "IDN", "ID": "IDN", "Indonesia": "IDN",
    "LAO": "LAO", "LA": "LAO", "Lao PDR": "LAO", "Laos": "LAO",
    "MYS": "MYS", "MY": "MYS", "Malaysia": "MYS",
    "MMR": "MMR", "MM": "MMR", "Myanmar": "MMR",
    "PHL": "PHL", "PH": "PHL", "Philippines": "PHL",
    "SGP": "SGP", "SG": "SGP", "Singapore": "SGP",
    "THA": "THA", "TH": "THA", "Thailand": "THA",
    "VNM": "VNM", "VN": "VNM", "Viet Nam": "VNM", "Vietnam": "VNM",
    "TLS": "TLS", "TL": "TLS", "Timor-Leste": "TLS"
}

# Rich ASEAN Country Dimension Data
ASEAN_COUNTRIES_META = {
    "BRN": {"CountryName": "Brunei Darussalam", "SubRegion": "Maritime ASEAN", "Capital": "Bandar Seri Begawan", "ISO2": "BN", "Latitude": 4.5353, "Longitude": 114.7277},
    "KHM": {"CountryName": "Cambodia", "SubRegion": "Mainland ASEAN", "Capital": "Phnom Penh", "ISO2": "KH", "Latitude": 12.5657, "Longitude": 104.9910},
    "IDN": {"CountryName": "Indonesia", "SubRegion": "Maritime ASEAN", "Capital": "Jakarta", "ISO2": "ID", "Latitude": -0.7893, "Longitude": 113.9213},
    "LAO": {"CountryName": "Lao PDR", "SubRegion": "Mainland ASEAN", "Capital": "Vientiane", "ISO2": "LA", "Latitude": 19.8563, "Longitude": 102.4955},
    "MYS": {"CountryName": "Malaysia", "SubRegion": "Maritime ASEAN", "Capital": "Kuala Lumpur", "ISO2": "MY", "Latitude": 4.2105, "Longitude": 101.9758},
    "MMR": {"CountryName": "Myanmar", "SubRegion": "Mainland ASEAN", "Capital": "Naypyidaw", "ISO2": "MM", "Latitude": 21.9162, "Longitude": 95.9560},
    "PHL": {"CountryName": "Philippines", "SubRegion": "Maritime ASEAN", "Capital": "Manila", "ISO2": "PH", "Latitude": 12.8797, "Longitude": 121.7740},
    "SGP": {"CountryName": "Singapore", "SubRegion": "Maritime ASEAN", "Capital": "Singapore", "ISO2": "SG", "Latitude": 1.3521, "Longitude": 103.8198},
    "THA": {"CountryName": "Thailand", "SubRegion": "Mainland ASEAN", "Capital": "Bangkok", "ISO2": "TH", "Latitude": 15.8700, "Longitude": 100.9925},
    "VNM": {"CountryName": "Viet Nam", "SubRegion": "Mainland ASEAN", "Capital": "Hanoi", "ISO2": "VN", "Latitude": 14.0583, "Longitude": 108.2772},
    "TLS": {"CountryName": "Timor-Leste", "SubRegion": "Observer Candidate", "Capital": "Dili", "ISO2": "TL", "Latitude": -8.5569, "Longitude": 125.5603}
}

def extract_unit(series_name):
    """Extract unit of measure from series name if enclosed in parentheses."""
    if not series_name:
        return "N/A"
    match = re.search(r'\((.*?)\)', series_name)
    if match:
        return match.group(1)
    if "%" in series_name:
        return "%"
    return "Absolute Unit"

def clean_val(val_str):
    if not val_str:
        return None
    val_clean = val_str.replace(" ", "").replace(",", "").strip()
    if val_clean in ['..', '', 'nan', 'NaN', 'null', 'NULL', '-']:
        return None
    try:
        return float(val_clean)
    except ValueError:
        return None

def resolve_country_code(text):
    """Accurately extract country ISO3 code using bracket regex or exact dictionary match."""
    if not text:
        return None
    # 1. Try bracket extraction e.g. "Malaysia [MY]" -> "MY"
    bracket_match = re.search(r'\[([A-Z]{2,3})\]', text)
    if bracket_match:
        iso_raw = bracket_match.group(1)
        if iso_raw in COUNTRY_CODE_MAP:
            return COUNTRY_CODE_MAP[iso_raw]
    
    # 2. Try exact name match
    cleaned_text = re.sub(r'\[.*?\]', '', text).strip()
    if cleaned_text in COUNTRY_CODE_MAP:
        return COUNTRY_CODE_MAP[cleaned_text]
        
    return None

def parse_tourism_file(file_path, domain):
    """
    Specialized parser for matrix-style dulich-Data.csv.
    Ignores summary rows ('Total Country (World)', 'Total Intra-ASEAN').
    Uses precise bracket ISO extraction to prevent substring mismatch.
    """
    print(f"Processing Tourism Matrix: {os.path.basename(file_path)}")
    fact_rows = []
    flow_rows = []
    master_rows = []
    indicator_dict = {}
    
    with open(file_path, mode='r', encoding='utf-8-sig', errors='ignore') as f:
        reader = csv.reader(f)
        header = None
        for row in reader:
            if row and any("Destination" in c or "Origin" in c for c in row):
                header = [c.strip() for c in row]
                break

        if not header or len(header) < 3:
            print("Warning: Dynamic header finder could not locate tourism matrix header.")
            return [], [], [], {}

        year_map = {}
        for idx in range(2, len(header)):
            m = re.search(r'(\d{4})', header[idx])
            if m:
                year_map[idx] = int(m.group(1))

        tot_arrivals_agg = {}
        current_dest = ""

        for row in reader:
            if not row or len(row) < 2:
                continue
            dest_col = row[0].strip()
            origin_col = row[1].strip()

            if dest_col:
                current_dest = dest_col
            
            if not current_dest or not origin_col:
                continue

            # SKIP summary rows!
            if origin_col.startswith("Total "):
                continue

            dest_code = resolve_country_code(current_dest)
            if not dest_code:
                continue

            origin_code = resolve_country_code(origin_col)
            if not origin_code:
                origin_code = origin_col

            series_code_tot = "ST.INT.ARVL.TOTL"
            indicator_dict[series_code_tot] = {
                "SeriesName": "Tổng lượt khách du lịch quốc tế nhập cảnh từ các nước ASEAN",
                "Domain": domain,
                "UnitOfMeasure": "Lượt khách (Person)"
            }

            for col_idx, yr in year_map.items():
                if col_idx < len(row):
                    clean_num = clean_val(row[col_idx])
                    if clean_num is not None:
                        # FIX: Skip self-referential rows (Origin == Destination)
                        if origin_code == dest_code:
                            continue
                        # Flow record
                        flow_rows.append({
                            "DestinationCountryCode": dest_code,
                            "OriginCountryCode": origin_code,
                            "Year": yr,
                            "Visitors": clean_num
                        })
                        # Accumulate total arrivals
                        key = (dest_code, yr)
                        tot_arrivals_agg[key] = tot_arrivals_agg.get(key, 0.0) + clean_num

        for (d_code, yr), tot_val in tot_arrivals_agg.items():
            # FIX: resolve proper country name from metadata (not ISO code)
            proper_name = ASEAN_COUNTRIES_META.get(d_code, {}).get("CountryName", d_code)
            fact_rows.append({
                "CountryCode": d_code,
                "SeriesCode": series_code_tot,
                "Year": yr,
                "Value": tot_val
            })
            master_rows.append({
                "CountryName": proper_name,  # FIX: use proper name, not code
                "CountryCode": d_code,
                "SeriesName": "Tổng lượt khách du lịch quốc tế nhập cảnh từ các nước ASEAN",
                "SeriesCode": series_code_tot,
                "Domain": domain,
                "Year": yr,
                "Value": tot_val
            })

    return fact_rows, flow_rows, master_rows, indicator_dict

def process_raw_data():
    print("=== STARTING DATA PREPROCESSING (WITH AUDITED ACCURACY) ===")
    
    fact_rows = []
    flow_rows = []
    country_dict = {}
    indicator_dict = {}
    years_set = set()
    master_rows = []

    for filename, domain in DOMAIN_MAPPING.items():
        file_path = os.path.join(RAW_DIR, filename)
        if not os.path.exists(file_path):
            print(f"Warning: File {filename} not found!")
            continue

        if filename == "dulich-Data.csv":
            t_fact, t_flow, t_master, t_ind = parse_tourism_file(file_path, domain)
            fact_rows.extend(t_fact)
            flow_rows.extend(t_flow)
            master_rows.extend(t_master)
            indicator_dict.update(t_ind)
            for r in t_master:
                years_set.add(r['Year'])
                country_dict[r['CountryCode']] = r['CountryName']
            continue

        print(f"Processing Standard Dataset: {filename}")
        with open(file_path, mode='r', encoding='utf-8-sig', errors='ignore') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header:
                continue

            header = [h.strip() for h in header]
            
            try:
                c_name_idx = header.index('Country Name')
                c_code_idx = header.index('Country Code')
                s_name_idx = header.index('Series Name')
                s_code_idx = header.index('Series Code')
            except ValueError as e:
                print(f"Skipping {filename}: Missing headers - {e}")
                continue

            year_col_map = {}
            for idx, col in enumerate(header):
                m = re.search(r'(\d{4})', col)
                if m and idx not in (c_name_idx, c_code_idx, s_name_idx, s_code_idx):
                    year_col_map[idx] = int(m.group(1))

            for row in reader:
                if not row or len(row) <= max(c_name_idx, c_code_idx, s_name_idx, s_code_idx):
                    continue

                country_name = row[c_name_idx].strip()
                country_code = row[c_code_idx].strip()
                series_name = row[s_name_idx].strip()
                series_code = row[s_code_idx].strip()

                if len(country_code) != 3 or not series_code:
                    continue

                if country_code not in country_dict:
                    country_dict[country_code] = country_name

                if series_code not in indicator_dict:
                    indicator_dict[series_code] = {
                        "SeriesName": series_name,
                        "Domain": domain,
                        "UnitOfMeasure": extract_unit(series_name)
                    }

                for col_idx, yr in year_col_map.items():
                    if col_idx < len(row):
                        raw_val = row[col_idx]
                        clean_num = clean_val(raw_val)
                        years_set.add(yr)

                        master_rows.append({
                            "CountryName": country_name,
                            "CountryCode": country_code,
                            "SeriesName": series_name,
                            "SeriesCode": series_code,
                            "Domain": domain,
                            "Year": yr,
                            "Value": clean_num if clean_num is not None else ""
                        })

                        if clean_num is not None:
                            fact_rows.append({
                                "CountryCode": country_code,
                                "SeriesCode": series_code,
                                "Year": yr,
                                "Value": clean_num
                            })

    # 1. FACT TABLE
    fact_path = os.path.join(CLEANED_DIR, "Fact_ASEAN_Indicators.csv")
    with open(fact_path, mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["CountryCode", "SeriesCode", "Year", "Value"])
        writer.writeheader()
        writer.writerows(fact_rows)

    # 1B. FACT TOURISM FLOW TABLE
    flow_path = os.path.join(CLEANED_DIR, "Fact_ASEAN_Tourism_Flow.csv")
    with open(flow_path, mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["DestinationCountryCode", "OriginCountryCode", "Year", "Visitors"])
        writer.writeheader()
        writer.writerows(flow_rows)

    # 2. DIM_COUNTRY
    dim_country_path = os.path.join(CLEANED_DIR, "Dim_Country.csv")
    dim_country_rows = []
    for code, cname in country_dict.items():
        meta = ASEAN_COUNTRIES_META.get(code, {
            "CountryName": cname, "SubRegion": "ASEAN", "Capital": "Unknown", "ISO2": code[:2], "Latitude": 0.0, "Longitude": 0.0
        })
        dim_country_rows.append({
            "CountryCode": code,
            "CountryName": cname if cname else meta["CountryName"],
            "SubRegion": meta["SubRegion"],
            "Capital": meta["Capital"],
            "ISO2": meta["ISO2"],
            "Latitude": meta["Latitude"],
            "Longitude": meta["Longitude"]
        })
    with open(dim_country_path, mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["CountryCode", "CountryName", "SubRegion", "Capital", "ISO2", "Latitude", "Longitude"])
        writer.writeheader()
        writer.writerows(dim_country_rows)

    # 3. DIM_INDICATOR
    dim_indicator_path = os.path.join(CLEANED_DIR, "Dim_Indicator.csv")
    dim_indicator_rows = []
    for scode, meta in indicator_dict.items():
        dim_indicator_rows.append({
            "SeriesCode": scode,
            "SeriesName": meta["SeriesName"],
            "Domain": meta["Domain"],
            "UnitOfMeasure": meta["UnitOfMeasure"]
        })
    with open(dim_indicator_path, mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["SeriesCode", "SeriesName", "Domain", "UnitOfMeasure"])
        writer.writeheader()
        writer.writerows(dim_indicator_rows)

    # 4. DIM_DATE
    dim_date_path = os.path.join(CLEANED_DIR, "Dim_Date.csv")
    dim_date_rows = []
    for yr in sorted(list(years_set)):
        dim_date_rows.append({
            "Year": yr,
            "Date": f"{yr}-01-01",
            "YearLabel": f"Năm {yr}",
            "Decade": f"Thập kỷ {(yr // 10) * 10}s",
            "Period": "2015-2020" if yr <= 2020 else "2021-2025"
        })
    with open(dim_date_path, mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Year", "Date", "YearLabel", "Decade", "Period"])
        writer.writeheader()
        writer.writerows(dim_date_rows)

    # 5. MASTER CLEANED FILE
    master_path = os.path.join(CLEANED_DIR, "ASEAN_Master_Cleaned.csv")
    with open(master_path, mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["CountryName", "CountryCode", "SeriesName", "SeriesCode", "Domain", "Year", "Value"])
        writer.writeheader()
        writer.writerows(master_rows)

    print("=== SUMMARY RESULTS ===")
    print(f"Fact_ASEAN_Indicators: {len(fact_rows)} records -> {fact_path}")
    print(f"Fact_ASEAN_Tourism_Flow: {len(flow_rows)} records -> {flow_path}")
    print(f"Dim_Country: {len(dim_country_rows)} records -> {dim_country_path}")
    print(f"Dim_Indicator: {len(dim_indicator_rows)} records -> {dim_indicator_path}")
    print(f"Dim_Date: {len(dim_date_rows)} records -> {dim_date_path}")
    print(f"ASEAN_Master_Cleaned: {len(master_rows)} records -> {master_path}")
    print("=== DATA PREPROCESSING COMPLETE ===")

if __name__ == "__main__":
    process_raw_data()
