import os
import sys
import csv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLEANED_DIR = os.path.join(BASE_DIR, "02_Data", "Cleaned")

def audit():
    print("=== STARTING DEEP DATASET AUDIT & INTEGRITY CHECK ===")
    
    fact_path = os.path.join(CLEANED_DIR, "Fact_ASEAN_Indicators.csv")
    flow_path = os.path.join(CLEANED_DIR, "Fact_ASEAN_Tourism_Flow.csv")
    country_path = os.path.join(CLEANED_DIR, "Dim_Country.csv")
    indicator_path = os.path.join(CLEANED_DIR, "Dim_Indicator.csv")
    date_path = os.path.join(CLEANED_DIR, "Dim_Date.csv")

    # 1. READ DIMENSIONS
    dim_countries = set()
    with open(country_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for r in reader:
            dim_countries.add(r['CountryCode'])

    dim_indicators = set()
    with open(indicator_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for r in reader:
            dim_indicators.add(r['SeriesCode'])

    dim_years = set()
    with open(date_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for r in reader:
            dim_years.add(int(r['Year']))

    print(f"[DIM CHECK] Dim_Country: {len(dim_countries)} codes | Dim_Indicator: {len(dim_indicators)} codes | Dim_Date: {len(dim_years)} years")

    # 2. AUDIT FACT_ASEAN_INDICATORS
    fact_keys = set()
    fact_duplicates = 0
    orphan_countries = set()
    orphan_indicators = set()
    orphan_years = set()
    invalid_values = 0
    total_fact_rows = 0

    with open(fact_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_fact_rows += 1
            ccode = row['CountryCode']
            scode = row['SeriesCode']
            yr = int(row['Year'])
            val_str = row['Value']

            # Duplicate composite key check
            key = (ccode, scode, yr)
            if key in fact_keys:
                fact_duplicates += 1
            else:
                fact_keys.add(key)

            # Orphan key checks
            if ccode not in dim_countries:
                orphan_countries.add(ccode)
            if scode not in dim_indicators:
                orphan_indicators.add(scode)
            if yr not in dim_years:
                orphan_years.add(yr)

            # Numeric value check
            try:
                val = float(val_str)
            except ValueError:
                invalid_values += 1

    print(f"\n--- AUDIT RESULTS FOR Fact_ASEAN_Indicators.csv ---")
    print(f"Total Rows: {total_fact_rows}")
    print(f"Unique Composite Keys: {len(fact_keys)}")
    print(f"Duplicate Composite Keys: {fact_duplicates} (Target: 0)")
    print(f"Orphan Country Keys: {len(orphan_countries)} {list(orphan_countries)}")
    print(f"Orphan Indicator Keys: {len(orphan_indicators)} {list(orphan_indicators)}")
    print(f"Orphan Year Keys: {len(orphan_years)} {list(orphan_years)}")
    print(f"Invalid Numeric Values: {invalid_values} (Target: 0)")

    # 3. AUDIT FACT_ASEAN_TOURISM_FLOW
    flow_keys = set()
    flow_duplicates = 0
    total_flow_rows = 0
    invalid_flow_vals = 0

    with open(flow_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_flow_rows += 1
            dcode = row['DestinationCountryCode']
            ocode = row['OriginCountryCode']
            yr = int(row['Year'])
            v_str = row['Visitors']

            key = (dcode, ocode, yr)
            if key in flow_keys:
                flow_duplicates += 1
            else:
                flow_keys.add(key)

            try:
                v = float(v_str)
            except ValueError:
                invalid_flow_vals += 1

    print(f"\n--- AUDIT RESULTS FOR Fact_ASEAN_Tourism_Flow.csv ---")
    print(f"Total Rows: {total_flow_rows}")
    print(f"Unique Composite Keys: {len(flow_keys)}")
    print(f"Duplicate Keys: {flow_duplicates} (Target: 0)")
    print(f"Invalid Visitor Values: {invalid_flow_vals} (Target: 0)")

    # 4. FINAL VERIFICATION VERDICT
    is_clean = (fact_duplicates == 0 and len(orphan_countries) == 0 and 
                len(orphan_indicators) == 0 and len(orphan_years) == 0 and 
                invalid_values == 0 and flow_duplicates == 0 and invalid_flow_vals == 0)

    print(f"\n=== OVERALL DATA PIPELINE VERDICT: {'100% PERFECT & CLEAN PASS' if is_clean else 'ISSUES DETECTED'} ===")

if __name__ == "__main__":
    audit()
