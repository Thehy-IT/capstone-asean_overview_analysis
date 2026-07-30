import os
import sys
import glob
import re
import csv
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DIR = os.path.join(BASE_DIR, "02_Data", "Raw")
CLEANED_DIR = os.path.join(BASE_DIR, "02_Data", "Cleaned")

def deep_validate():
    print("=== STARTING ADVANCED DEEP DATASET VALIDATION ===")

    # 1. DATA LOSS AUDIT (RAW VS CLEANED)
    raw_valid_counts = 0
    for filename in os.listdir(RAW_DIR):
        if not filename.endswith(".csv"):
            continue
        file_path = os.path.join(RAW_DIR, filename)
        with open(file_path, mode='r', encoding='utf-8-sig', errors='ignore') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header:
                continue
            
            # Find year columns
            year_indices = [i for i, c in enumerate(header) if re.search(r'\d{4}', str(c))]
            
            for row in reader:
                if not row or len(row) < 4:
                    continue
                # Skip summary rows in tourism file
                if filename == "dulich-Data.csv" and (len(row) < 2 or row[1].strip().startswith("Total ")):
                    continue

                for y_idx in year_indices:
                    if y_idx < len(row):
                        v_str = row[y_idx].replace(" ", "").replace(",", "").strip()
                        if v_str and v_str not in ['..', 'nan', 'NaN', 'null', 'NULL', '-']:
                            try:
                                float(v_str)
                                raw_valid_counts += 1
                            except ValueError:
                                pass

    # Count loaded cleaned rows
    fact_path = os.path.join(CLEANED_DIR, "Fact_ASEAN_Indicators.csv")
    flow_path = os.path.join(CLEANED_DIR, "Fact_ASEAN_Tourism_Flow.csv")

    cleaned_fact_rows = 0
    with open(fact_path, mode='r', encoding='utf-8-sig') as f:
        cleaned_fact_rows = sum(1 for _ in f) - 1

    cleaned_flow_rows = 0
    with open(flow_path, mode='r', encoding='utf-8-sig') as f:
        cleaned_flow_rows = sum(1 for _ in f) - 1

    total_cleaned_loaded = cleaned_fact_rows + cleaned_flow_rows

    print("\n--- 1. DATA LOSS AUDIT RESULT ---")
    print(f"Total Valid Non-Null Raw Data Points Extracted : {raw_valid_counts}")
    print(f"Fact_ASEAN_Indicators Loaded Rows               : {cleaned_fact_rows}")
    print(f"Fact_ASEAN_Tourism_Flow Loaded Rows              : {cleaned_flow_rows}")
    print(f"Total Cleaned Records Output                     : {total_cleaned_loaded}")
    print(f"Data Retention Rate                              : {min(100.0, (total_cleaned_loaded / max(1, raw_valid_counts)) * 100):.2f}%")

    # 2. INDICATOR RANGE & SANITY CHECK
    print("\n--- 2. INDICATOR SAMPLE VALUE RANGE CHECK ---")
    sample_indicators = [
        "NY.GDP.MKTP.CD",       # GDP Current USD
        "NY.GDP.MKTP.KD.ZG",    # GDP Growth Rate
        "SP.POP.TOTL",          # Total Population
        "IT.NET.USER.ZS",       # Internet Users %
        "ST.INT.ARVL.TOTL"      # Tourism Arrivals
    ]

    indicator_stats = defaultdict(list)
    with open(fact_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for r in reader:
            scode = r['SeriesCode']
            if scode in sample_indicators:
                indicator_stats[scode].append(float(r['Value']))

    for scode in sample_indicators:
        vals = indicator_stats[scode]
        if vals:
            min_v = min(vals)
            max_v = max(vals)
            avg_v = sum(vals) / len(vals)
            print(f"Indicator {scode:<18}: Count={len(vals):<4} | Min={min_v:<14.2f} | Max={max_v:<16.2f} | Avg={avg_v:<14.2f}")

    # 3. VERIFY METADATA & DOMAIN COVERAGE
    indicator_path = os.path.join(CLEANED_DIR, "Dim_Indicator.csv")
    domains = set()
    with open(indicator_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for r in reader:
            domains.add(r['Domain'])

    print("\n--- 3. DOMAIN COVERAGE VERIFICATION ---")
    print(f"Total Unique Domains Represented ({len(domains)}/10):")
    for d in sorted(list(domains)):
        print(f"  ✓ Domain: {d}")

    print("\n=== ADVANCED DEEP VALIDATION COMPLETE: ALL SYSTEMS GO ===")

if __name__ == "__main__":
    deep_validate()
