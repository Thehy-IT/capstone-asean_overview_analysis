"""
DEEP DATA QUALITY AUDIT v2 — Senior Data Analyst
ASEAN Project: Complete validation before Power BI import
Checks: value ranges, coverage matrix, outliers, encoding, 
        data type consistency, logical coherence, master-vs-fact diff
"""
import csv, os, sys, collections, math

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLEANED = os.path.join(BASE, "02_Data", "Cleaned")

def load(filename):
    with open(os.path.join(CLEANED, filename), encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

COUNTRY_CODES = ['BRN','KHM','IDN','LAO','MYS','MMR','PHL','SGP','THA','VNM','TLS']
YEARS = list(range(2015, 2026))

EXPECTED_INDICATORS = {
    # code: (domain, expected_min, expected_max, unit_hint)
    "NY.GDP.MKTP.CD":       ("Kinh tế & GDP", 1e9, 2e12, "USD"),
    "NY.GDP.MKTP.KD.ZG":   ("Kinh tế & GDP", -15, 15, "%"),
    "NY.GDP.PCAP.CD":       ("Kinh tế & GDP", 500, 80000, "USD/cap"),
    "FP.CPI.TOTL.ZG":      ("Kinh tế & GDP", -5, 60, "%"),
    "GC.DOD.TOTL.GD.ZS":   ("Kinh tế & GDP", 0, 120, "% GDP"),
    "NE.GDI.TOTL.ZS":      ("Kinh tế & GDP", 0, 70, "% GDP"),
    "NY.GNS.ICTR.ZS":      ("Kinh tế & GDP", -20, 60, "% GDP"),
    "SP.POP.TOTL":         ("Dân số & Nhân khẩu học", 1e5, 3e8, "persons"),
    "SP.POP.GROW":         ("Dân số & Nhân khẩu học", -5, 5, "%"),
    "SP.URB.TOTL.IN.ZS":   ("Dân số & Nhân khẩu học", 0, 100, "%"),
    "SP.DYN.TFRT.IN":      ("Dân số & Nhân khẩu học", 0.5, 7, "births/woman"),
    "IT.NET.USER.ZS":      ("Công nghệ & Hạ tầng số", 0, 100, "%"),
    "IT.CEL.SETS.P2":      ("Công nghệ & Hạ tầng số", 0, 200, "per 100"),
    "IT.NET.BBND.P2":      ("Công nghệ & Hạ tầng số", 0, 100, "per 100"),
    "IT.NET.SECR.P6":      ("Công nghệ & Hạ tầng số", 0, 1e6, "per 1M"),
    "SL.TLF.CACT.ZS":      ("Lao động & Việc làm", 40, 90, "%"),
    "SL.UEM.TOTL.ZS":      ("Lao động & Việc làm", 0, 25, "%"),
    "SL.UEM.1524.ZS":      ("Lao động & Việc làm", 0, 60, "%"),
    "SL.AGR.EMPL.ZS":      ("Lao động & Việc làm", 0, 80, "%"),
    "SL.IND.EMPL.ZS":      ("Lao động & Việc làm", 0, 60, "%"),
    "SL.SRV.EMPL.ZS":      ("Lao động & Việc làm", 0, 90, "%"),
    "EG.ELC.ACCS.ZS":      ("Môi trường & Năng lượng", 0, 100, "%"),
    "EG.FEC.RNEW.ZS":      ("Môi trường & Năng lượng", 0, 100, "%"),
    "AG.LND.FRST.ZS":      ("Môi trường & Năng lượng", 0, 100, "%"),
    "NY.ADJ.DCO2.GN.ZS":   ("Môi trường & Năng lượng", 0, 20, "% GNI"),
    "NE.EXP.GNFS.CD":      ("Thương mại & Xuất nhập khẩu", 1e8, 1e12, "USD"),
    "NE.IMP.GNFS.CD":      ("Thương mại & Xuất nhập khẩu", 1e8, 1e12, "USD"),
    "NE.TRD.GNFS.ZS":      ("Thương mại & Xuất nhập khẩu", 0, 400, "% GDP"),
    "BX.KLT.DINV.CD.WD":   ("Đầu tư trực tiếp nước ngoài (FDI)", -2e10, 2e11, "USD"),
    "SE.ADT.LITR.ZS":      ("Giáo dục & Đào tạo", 50, 100, "%"),
    "SE.PRM.ENRR":         ("Giáo dục & Đào tạo", 50, 130, "% gross"),
    "SP.DYN.LE00.IN":      ("Y tế & Sức khỏe", 50, 90, "years"),
    "SH.XPD.CHEX.GD.ZS":  ("Y tế & Sức khỏe", 0, 15, "% GDP"),
    "SH.DYN.MORT":         ("Y tế & Sức khỏe", 0, 100, "per 1000"),
    "SH.MED.BEDS.ZS":      ("Y tế & Sức khỏe", 0, 15, "per 1000"),
    "ST.INT.ARVL.TOTL":    ("Du lịch & Dịch vụ", 0, 5e7, "persons"),
}

print("=" * 70)
print("DEEP AUDIT v2 — ASEAN Pre-PowerBI Full Validation")
print("=" * 70)

facts = load("Fact_ASEAN_Indicators.csv")
tourism = load("Fact_ASEAN_Tourism_Flow.csv")
dim_country = load("Dim_Country.csv")
dim_indicator = load("Dim_Indicator.csv")
dim_date = load("Dim_Date.csv")
master = load("ASEAN_Master_Cleaned.csv")

# ─── A. COVERAGE MATRIX ───────────────────────────────────────────────────────
print("\n=== A. COVERAGE MATRIX (Country x Year completeness) ===")
# Build lookup: (country, year) -> set of series codes
coverage = collections.defaultdict(set)
for r in facts:
    coverage[(r['CountryCode'], r['Year'])].add(r['SeriesCode'])

total_indicators = 65
print(f"  Expected 65 indicators per (Country, Year) cell")
print(f"  {'Country':<8} | " + " | ".join(str(y) for y in YEARS))
print(f"  {'-------':<8}-+-" + "-+-".join(["----"]*11))

sparse_cells = []
for cc in COUNTRY_CODES:
    row_str = f"  {cc:<8} | "
    cells = []
    for yr in YEARS:
        n = len(coverage.get((cc, str(yr)), set()))
        cells.append(f"{n:>4}")
        if n < 30:  # less than 30 indicators = very sparse
            sparse_cells.append((cc, yr, n))
    row_str += " | ".join(cells)
    print(row_str)

if sparse_cells:
    print(f"\n  SPARSE CELLS (<30 indicators):")
    for cc, yr, n in sparse_cells:
        print(f"    {cc} {yr}: only {n} indicators")

# ─── B. OUTLIER / LOGICAL RANGE CHECKS ───────────────────────────────────────
print("\n=== B. VALUE RANGE VALIDATION (Logical Sanity Checks) ===")
fact_lookup = {}
for r in facts:
    key = (r['CountryCode'], r['SeriesCode'], r['Year'])
    fact_lookup[key] = float(r['Value']) if r['Value'] else None

outliers = []
for sc, (domain, vmin, vmax, unit) in EXPECTED_INDICATORS.items():
    for r in facts:
        if r['SeriesCode'] != sc:
            continue
        try:
            val = float(r['Value'])
        except (ValueError, TypeError):
            continue
        if val < vmin or val > vmax:
            outliers.append({
                'code': sc, 'country': r['CountryCode'],
                'year': r['Year'], 'value': val,
                'expected': f"{vmin}–{vmax} {unit}"
            })

if outliers:
    print(f"  OUTLIERS DETECTED: {len(outliers)} values outside expected range")
    for o in outliers[:20]:
        print(f"    {o['country']} {o['year']} [{o['code']}]: {o['value']:,.2f} (expected {o['expected']})")
    if len(outliers) > 20:
        print(f"    ... and {len(outliers)-20} more")
else:
    print("  All checked values within logical range — OK")

# ─── C. EMPLOYMENT SECTOR COHERENCE (Agri + Industry + Services ≈ 100%) ───────
print("\n=== C. EMPLOYMENT SECTOR COHERENCE CHECK (sum ≈ 100%) ===")
sector_codes = ["SL.AGR.EMPL.ZS", "SL.IND.EMPL.ZS", "SL.SRV.EMPL.ZS"]
coherence_issues = []
for cc in COUNTRY_CODES:
    for yr in [str(y) for y in YEARS]:
        vals = []
        for sc in sector_codes:
            v = fact_lookup.get((cc, sc, yr))
            if v is not None:
                vals.append(v)
        if len(vals) == 3:
            total = sum(vals)
            if abs(total - 100) > 2.0:  # allow ±2% rounding tolerance
                coherence_issues.append((cc, yr, total, vals))

if coherence_issues:
    print(f"  WARN: {len(coherence_issues)} country-year combos where Agri+Industry+Services != 100% (±2%)")
    for cc, yr, tot, vals in coherence_issues[:5]:
        print(f"    {cc} {yr}: {vals[0]:.1f}+{vals[1]:.1f}+{vals[2]:.1f}={tot:.1f}%")
else:
    print("  All employment sector sums within ±2% tolerance — OK")

# ─── D. POPULATION GENDER COHERENCE (Male% + Female% ≈ 100%) ─────────────────
print("\n=== D. POPULATION GENDER SPLIT COHERENCE CHECK ===")
gender_codes = ["SP.POP.TOTL.FE.ZS", "SP.POP.TOTL.MA.ZS"]
gender_issues = []
for cc in COUNTRY_CODES:
    for yr in [str(y) for y in YEARS]:
        fe = fact_lookup.get((cc, "SP.POP.TOTL.FE.ZS", yr))
        ma = fact_lookup.get((cc, "SP.POP.TOTL.MA.ZS", yr))
        if fe is not None and ma is not None:
            total = fe + ma
            if abs(total - 100) > 0.5:
                gender_issues.append((cc, yr, fe, ma, total))

if gender_issues:
    print(f"  WARN: {len(gender_issues)} combos where Female%+Male% != 100%")
    for cc, yr, fe, ma, tot in gender_issues[:5]:
        print(f"    {cc} {yr}: {fe:.2f}+{ma:.2f}={tot:.2f}")
else:
    print("  All gender % sums within ±0.5% tolerance — OK")

# ─── E. TOURISM FLOW COVERAGE & STATS ────────────────────────────────────────
print("\n=== E. TOURISM FLOW DEEP ANALYSIS ===")
print(f"  Total rows: {len(tourism)}")
year_cnt = collections.Counter(r['Year'] for r in tourism)
print(f"  Rows by year: {dict(sorted(year_cnt.items()))}")
# Expected: 11 dest x 10 origin = 110 pairs per year (excluding self)
for yr in sorted(year_cnt.keys()):
    cnt = year_cnt[yr]
    if cnt != 110:
        print(f"  WARN Year {yr}: {cnt} rows (expected 110 for 11x10 matrix)")

# Check for missing corridors (e.g. SGP->MYS always present?)
key_corridors = [('SGP','MYS'),('MYS','THA'),('IDN','MYS'),('THA','MYS')]
print(f"  Key corridor presence check:")
for dest, orig in key_corridors:
    years_present = [r['Year'] for r in tourism 
                     if r['DestinationCountryCode']==dest and r['OriginCountryCode']==orig]
    print(f"    {orig}→{dest}: {sorted(years_present)}")

# Check for suspiciously LOW values (< 10 visitors = likely data artifact)
tiny_vals = [r for r in tourism if float(r['Visitors']) < 10]
if tiny_vals:
    print(f"  WARN: {len(tiny_vals)} rows with Visitors < 10 (possible data artifact):")
    for r in tiny_vals[:5]:
        print(f"    {r['OriginCountryCode']}→{r['DestinationCountryCode']} {r['Year']}: {r['Visitors']}")
        
# Check COVID dip: 2020-2021 should be much lower than 2019
total_by_year = {}
for r in tourism:
    yr = r['Year']
    total_by_year[yr] = total_by_year.get(yr, 0) + float(r['Visitors'])
print(f"  Total Visitors by year:")
for yr in sorted(total_by_year.keys()):
    bar = '#' * int(total_by_year[yr] / 2000000)
    print(f"    {yr}: {total_by_year[yr]:>15,.0f}  {bar}")

# ─── F. MASTER CSV vs FACT TABLE DIFF CHECK ─────────────────────────────────
print("\n=== F. MASTER CSV vs FACT TABLE CONSISTENCY ===")
master_facts = {(r['CountryCode'], r['SeriesCode'], str(r['Year'])) 
                for r in master if r['Value'] and r['Value'].strip() != ''}
fact_keys = {(r['CountryCode'], r['SeriesCode'], r['Year']) for r in facts}

in_master_not_fact = master_facts - fact_keys
in_fact_not_master = fact_keys - master_facts

print(f"  Master (non-null records): {len(master_facts)}")
print(f"  Fact_ASEAN_Indicators: {len(fact_keys)}")
if in_master_not_fact:
    print(f"  WARN: {len(in_master_not_fact)} records in Master but not in Fact (value != null in master but absent in fact)")
    for k in list(in_master_not_fact)[:5]:
        print(f"    {k}")
else:
    print("  Master non-null records all present in Fact — OK")
if in_fact_not_master:
    print(f"  WARN: {len(in_fact_not_master)} records in Fact but not in Master")
else:
    print("  All Fact records present in Master — OK")

# ─── G. ENCODING & SPECIAL CHARACTER CHECK ───────────────────────────────────
print("\n=== G. ENCODING & FIELD FORMAT CHECKS ===")
# Check Year is integer (not float like 2015.0)
year_format_bugs = []
for r in facts:
    try:
        y = r['Year']
        if '.' in y:
            year_format_bugs.append(y)
    except:
        pass
if year_format_bugs:
    print(f"  BUG: Year stored as float string: {year_format_bugs[:5]}")
else:
    print("  Year format (integer): OK")

# Check Value format — no trailing spaces, no commas in numbers
value_format_bugs = [r for r in facts if ' ' in r['Value'] or ',' in r['Value']]
if value_format_bugs:
    print(f"  BUG: Value has spaces/commas: {[r['Value'] for r in value_format_bugs[:3]]}")
else:
    print("  Value format (no spaces/commas): OK")

# Check Dim_Country encoding
country_check = load("Dim_Country.csv")
print(f"  Dim_Country CountryName spot check:")
for r in country_check:
    print(f"    {r['CountryCode']} → '{r['CountryName']}' | Lat={r['Latitude']} Lon={r['Longitude']}")

# Check lat/lon are valid floats
latlon_bugs = []
for r in country_check:
    try:
        lat = float(r['Latitude'])
        lon = float(r['Longitude'])
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            latlon_bugs.append(r['CountryCode'])
    except:
        latlon_bugs.append(r['CountryCode'])
if latlon_bugs:
    print(f"  BUG: Invalid lat/lon for: {latlon_bugs}")
else:
    print("  Lat/Lon valid float values: OK")

# ─── H. MYANMAR COMPLETENESS CONCERN ─────────────────────────────────────────
print("\n=== H. MYANMAR (MMR) SPARSE DATA CONCERN ===")
mmr_series = {r['SeriesCode'] for r in facts if r['CountryCode'] == 'MMR'}
all_series = {r['SeriesCode'] for r in facts}
mmr_missing = all_series - mmr_series
print(f"  MMR has data for {len(mmr_series)}/{len(all_series)} indicators")
if mmr_missing:
    print(f"  MMR missing indicators: {sorted(mmr_missing)}")

mmr_by_year = collections.Counter(r['Year'] for r in facts if r['CountryCode'] == 'MMR')
print(f"  MMR records by year: {dict(sorted(mmr_by_year.items()))}")

# ─── I. TIMOR-LESTE COMPLETENESS CONCERN ─────────────────────────────────────
print("\n=== I. TIMOR-LESTE (TLS) SPARSE DATA CONCERN ===")
tls_series = {r['SeriesCode'] for r in facts if r['CountryCode'] == 'TLS'}
tls_missing = all_series - tls_series
print(f"  TLS has data for {len(tls_series)}/{len(all_series)} indicators")
if tls_missing:
    print(f"  TLS missing indicators: {sorted(tls_missing)}")

# ─── J. YEAR 2025 DATA QUALITY ───────────────────────────────────────────────
print("\n=== J. YEAR 2025 DATA COMPLETENESS ===")
y2025 = [r for r in facts if r['Year'] == '2025']
y2024 = [r for r in facts if r['Year'] == '2024']
print(f"  Records 2024: {len(y2024)} | Records 2025: {len(y2025)}")
series_2025 = {r['SeriesCode'] for r in y2025}
series_2024 = {r['SeriesCode'] for r in y2024}
missing_in_2025 = series_2024 - series_2025
print(f"  Indicators present in 2024 but missing in 2025: {len(missing_in_2025)}")
if missing_in_2025:
    for sc in sorted(missing_in_2025)[:10]:
        print(f"    {sc}")
    if len(missing_in_2025) > 10:
        print(f"    ... and {len(missing_in_2025)-10} more")
cc_2025 = collections.Counter(r['CountryCode'] for r in y2025)
print(f"  Countries with 2025 data: {dict(sorted(cc_2025.items()))}")

# ─── K. FINAL SCORE ──────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("DEEP AUDIT v2 COMPLETE")
print("=" * 70)
