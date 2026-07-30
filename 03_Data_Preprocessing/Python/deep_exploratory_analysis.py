import os
import sys
import csv
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLEANED_DIR = os.path.join(BASE_DIR, "02_Data", "Cleaned")

def deep_eda():
    print("=== DEEP EXPLORATORY DATA ANALYSIS (SENIOR DATA ANALYST INSIGHTS) ===")

    fact_path = os.path.join(CLEANED_DIR, "Fact_ASEAN_Indicators.csv")
    flow_path = os.path.join(CLEANED_DIR, "Fact_ASEAN_Tourism_Flow.csv")
    country_path = os.path.join(CLEANED_DIR, "Dim_Country.csv")
    indicator_path = os.path.join(CLEANED_DIR, "Dim_Indicator.csv")

    c_names = {}
    with open(country_path, mode='r', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            c_names[r['CountryCode']] = r['CountryName']

    ind_names = {}
    with open(indicator_path, mode='r', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            ind_names[r['SeriesCode']] = r['SeriesName']

    # Load Fact Data into structured dictionary: (scode, ccode, year) -> value
    data = defaultdict(dict)
    with open(fact_path, mode='r', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            scode = r['SeriesCode']
            ccode = r['CountryCode']
            yr = int(r['Year'])
            val = float(r['Value'])
            data[scode][(ccode, yr)] = val

    # -------------------------------------------------------------------------
    # EXPLORATION 1: ASEAN TOTAL GDP TRAJECTORY (2015 vs 2019 vs 2023)
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("1. ASEAN TOTAL GDP & ECONOMIC CONCENTRATION (2015 - 2023)")
    print("="*80)
    
    gdp_code = "NY.GDP.MKTP.CD"
    years_to_check = [2015, 2019, 2023]
    
    for yr in years_to_check:
        total_gdp = sum(data[gdp_code].get((c, yr), 0) for c in c_names)
        print(f"\n--- Total ASEAN GDP ({yr}): ${total_gdp / 1e12:.3f} Trillion USD ---")
        
        # Sort countries by GDP in that year
        country_gdps = []
        for c in c_names:
            v = data[gdp_code].get((c, yr), 0)
            if v > 0:
                share = (v / total_gdp) * 100 if total_gdp > 0 else 0
                country_gdps.append((c_names[c], v / 1e9, share))
        
        country_gdps.sort(key=lambda x: x[1], reverse=True)
        top3_share = sum(x[2] for x in country_gdps[:3])
        print(f"Top 3 Economies Concentration ({country_gdps[0][0]}, {country_gdps[1][0]}, {country_gdps[2][0]}): {top3_share:.2f}% of ASEAN GDP")
        
        for cname, gdp_b, share in country_gdps[:5]:
            print(f"  - {cname:<20}: ${gdp_b:<8.2f}B USD ({share:.2f}%)")

    # -------------------------------------------------------------------------
    # EXPLORATION 2: DIGITAL LEAPFROGGING - INTERNET PENETRATION JUMP (2015 VS 2023)
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("2. DIGITAL TRANSFORMATION: INTERNET USER PENETRATION (% POPULATION)")
    print("="*80)
    
    net_code = "IT.NET.USER.ZS"
    net_jumps = []
    for c in c_names:
        v_2015 = data[net_code].get((c, 2015), None)
        v_2023 = data[net_code].get((c, 2023), None)
        if v_2015 is not None and v_2023 is not None:
            jump = v_2023 - v_2015
            net_jumps.append((c_names[c], v_2015, v_2023, jump))
            
    net_jumps.sort(key=lambda x: x[3], reverse=True)
    print(f"{'Country':<20} | {'2015 %':<10} | {'2023 %':<10} | {'Percentage Point Jump':<22}")
    print("-" * 70)
    for cname, v15, v23, jump in net_jumps:
        print(f"{cname:<20} | {v15:<10.2f}% | {v23:<10.2f}% | +{jump:<21.2f}%")

    # -------------------------------------------------------------------------
    # EXPLORATION 3: TOURISM MATRIX FLOW - PRE-COVID vs COVID vs RECOVERY
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("3. INTRA-ASEAN TOURISM FLOW CORRIDORS (PRE-COVID 2019 VS RECOVERY 2023)")
    print("="*80)
    
    flow_2019 = defaultdict(float)
    flow_2023 = defaultdict(float)
    
    with open(flow_path, mode='r', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            dcode = r['DestinationCountryCode']
            ocode = r['OriginCountryCode']
            yr = int(r['Year'])
            vis = float(r['Visitors'])
            
            key = (c_names.get(dcode, dcode), c_names.get(ocode, ocode))
            if yr == 2019:
                flow_2019[key] += vis
            elif yr == 2023:
                flow_2023[key] += vis

    print("\n--- TOP 5 INTRA-ASEAN TOURISM CORRIDORS IN 2019 (PRE-COVID PEAK) ---")
    top_2019 = sorted(flow_2019.items(), key=lambda x: x[1], reverse=True)[:5]
    for (dest, orig), vis in top_2019:
        print(f"  - {orig}  --->  {dest}: {vis:,.0f} visitors")

    print("\n--- TOP 5 INTRA-ASEAN TOURISM CORRIDORS IN 2023 (RECOVERY) ---")
    top_2023 = sorted(flow_2023.items(), key=lambda x: x[1], reverse=True)[:5]
    for (dest, orig), vis in top_2023:
        print(f"  - {orig}  --->  {dest}: {vis:,.0f} visitors")

    print("\n=== DEEP EXPLORATORY DATA ANALYSIS COMPLETED ===")

if __name__ == "__main__":
    deep_eda()
