"""
FULL DATA QUALITY AUDIT SCRIPT
Senior Data Analyst - ASEAN Project Pre-PowerBI Validation
"""
import csv
import collections
import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLEANED = os.path.join(BASE, "02_Data", "Cleaned")

def load_csv(filename):
    path = os.path.join(CLEANED, filename)
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def audit():
    print("=" * 70)
    print("FULL DATA QUALITY AUDIT — ASEAN PROJECT (Pre-PowerBI)")
    print("=" * 70)

    # ── 1. DIM_COUNTRY ────────────────────────────────────────────────────
    print("\n[1] DIM_COUNTRY")
    countries = load_csv("Dim_Country.csv")
    print(f"  Rows: {len(countries)}")
    bugs = []
    for r in countries:
        if r["CountryName"] == r["CountryCode"]:
            bugs.append(f"    BUG CountryName==CountryCode: {r['CountryCode']}")
        if not r["Latitude"] or not r["Longitude"]:
            bugs.append(f"    MISSING Lat/Lon: {r['CountryCode']}")
        if r["SubRegion"] not in ("Mainland ASEAN", "Maritime ASEAN", "Observer Candidate"):
            bugs.append(f"    BAD SubRegion '{r['SubRegion']}': {r['CountryCode']}")
    if bugs:
        for b in bugs: print(b)
    else:
        print("  ✓ No critical bugs found")

    country_codes = {r["CountryCode"] for r in countries}
    print(f"  Distinct CountryCodes: {sorted(country_codes)}")

    # ── 2. DIM_DATE ────────────────────────────────────────────────────────
    print("\n[2] DIM_DATE")
    dates = load_csv("Dim_Date.csv")
    print(f"  Rows: {len(dates)}")
    years = [int(r["Year"]) for r in dates]
    print(f"  Year range: {min(years)} – {max(years)}")
    dup_years = [y for y, c in collections.Counter(years).items() if c > 1]
    if dup_years:
        print(f"  BUG: Duplicate years: {dup_years}")
    else:
        print("  ✓ No duplicate years")
    # Check Period logic
    period_bugs = []
    for r in dates:
        y = int(r["Year"])
        expected = "2015-2020" if y <= 2020 else "2021-2025"
        if r["Period"] != expected:
            period_bugs.append(f"    BUG Period: Year={y}, got '{r['Period']}', expected '{expected}'")
    if period_bugs:
        for b in period_bugs: print(b)
    else:
        print("  ✓ Period column logic correct")
    # Year 2020 in Decade check
    for r in dates:
        if int(r["Year"]) == 2020 and "2010" not in r["Decade"]:
            print(f"  WARN: Year 2020 in Decade '{r['Decade']}' — should be Thập kỷ 2010s or 2020s?")

    # ── 3. DIM_INDICATOR ──────────────────────────────────────────────────
    print("\n[3] DIM_INDICATOR")
    indicators = load_csv("Dim_Indicator.csv")
    print(f"  Rows: {len(indicators)}")
    series_codes = {r["SeriesCode"] for r in indicators}
    dup_codes = [c for c, n in collections.Counter(r["SeriesCode"] for r in indicators).items() if n > 1]
    if dup_codes:
        print(f"  BUG: Duplicate SeriesCodes: {dup_codes}")
    else:
        print("  ✓ No duplicate SeriesCodes")
    domains = collections.Counter(r["Domain"] for r in indicators)
    print(f"  Domains ({len(domains)}):")
    for d, c in sorted(domains.items(), key=lambda x: -x[1]):
        print(f"    {d}: {c} indicators")
    missing_unit = [r["SeriesCode"] for r in indicators if not r["UnitOfMeasure"] or r["UnitOfMeasure"] == "N/A"]
    if missing_unit:
        print(f"  WARN: Missing UnitOfMeasure: {missing_unit}")

    # ── 4. FACT_ASEAN_INDICATORS ──────────────────────────────────────────
    print("\n[4] FACT_ASEAN_INDICATORS")
    facts = load_csv("Fact_ASEAN_Indicators.csv")
    print(f"  Total rows: {len(facts)}")

    # Null check
    null_vals = [r for r in facts if not r["Value"] or r["Value"].strip() == ""]
    print(f"  Null Value rows: {len(null_vals)}")

    # FK check — CountryCode
    fact_countries = {r["CountryCode"] for r in facts}
    orphan_cc = fact_countries - country_codes
    if orphan_cc:
        print(f"  BUG FK CountryCode not in Dim_Country: {orphan_cc}")
    else:
        print(f"  ✓ All {len(fact_countries)} CountryCodes join to Dim_Country")

    # FK check — SeriesCode
    fact_series = {r["SeriesCode"] for r in facts}
    orphan_sc = fact_series - series_codes
    if orphan_sc:
        print(f"  BUG FK SeriesCode not in Dim_Indicator: {orphan_sc}")
    else:
        print(f"  ✓ All {len(fact_series)} SeriesCodes join to Dim_Indicator")

    # FK check — Year
    date_years = {str(r["Year"]) for r in dates}
    fact_years_orphan = {r["Year"] for r in facts if r["Year"] not in date_years}
    if fact_years_orphan:
        print(f"  BUG FK Year not in Dim_Date: {sorted(fact_years_orphan)}")
    else:
        print(f"  ✓ All Years join to Dim_Date")

    # Duplicate grain check
    grains = [(r["CountryCode"], r["SeriesCode"], r["Year"]) for r in facts]
    dup_grains = [(g, c) for g, c in collections.Counter(grains).items() if c > 1]
    if dup_grains:
        print(f"  BUG: {len(dup_grains)} duplicate grains (CountryCode, SeriesCode, Year)!")
        for g, c in dup_grains[:5]:
            print(f"    {g} x{c}")
    else:
        print("  ✓ No duplicate grain keys")

    # Year distribution
    year_dist = collections.Counter(r["Year"] for r in facts)
    print(f"  Year range in facts: {min(year_dist.keys())} – {max(year_dist.keys())}")
    year_2025 = year_dist.get("2025", 0)
    print(f"  Records for year 2025: {year_2025} (NOTE: World Bank data may be forecast/null)")

    # CountryCode distribution
    cc_dist = collections.Counter(r["CountryCode"] for r in facts)
    print(f"  Records per country:")
    for cc, cnt in sorted(cc_dist.items()):
        print(f"    {cc}: {cnt} records")

    # ── 5. FACT_ASEAN_TOURISM_FLOW ─────────────────────────────────────────
    print("\n[5] FACT_ASEAN_TOURISM_FLOW")
    tourism = load_csv("Fact_ASEAN_Tourism_Flow.csv")
    print(f"  Total rows: {len(tourism)}")

    # FK checks
    tour_dest = {r["DestinationCountryCode"] for r in tourism}
    tour_orig = {r["OriginCountryCode"] for r in tourism}
    orphan_dest = tour_dest - country_codes
    orphan_orig = tour_orig - country_codes
    if orphan_dest:
        print(f"  BUG FK DestinationCountryCode not in Dim_Country: {orphan_dest}")
    else:
        print(f"  ✓ All DestinationCodes valid")
    if orphan_orig:
        print(f"  BUG FK OriginCountryCode not in Dim_Country: {orphan_orig}")
    else:
        print(f"  ✓ All OriginCodes valid ({len(tour_orig)} unique origins)")

    # Self-referential check
    self_ref = [r for r in tourism if r["DestinationCountryCode"] == r["OriginCountryCode"]]
    if self_ref:
        print(f"  WARN: {len(self_ref)} self-referential rows (same Origin=Destination):")
        for r in self_ref[:3]:
            print(f"    {r}")

    # Grain duplicate check
    tour_grains = [(r["DestinationCountryCode"], r["OriginCountryCode"], r["Year"]) for r in tourism]
    dup_tour = [(g, c) for g, c in collections.Counter(tour_grains).items() if c > 1]
    if dup_tour:
        print(f"  BUG: {len(dup_tour)} duplicate tourism grains!")
    else:
        print("  ✓ No duplicate tourism grains")

    # Null visitors
    null_vis = [r for r in tourism if not r["Visitors"] or r["Visitors"].strip() == ""]
    print(f"  Null Visitors: {len(null_vis)}")

    # Year range
    tour_years = sorted({r["Year"] for r in tourism})
    print(f"  Year range: {tour_years[0]} – {tour_years[-1]}")

    # ── 6. MASTER CSV CONSISTENCY ──────────────────────────────────────────
    print("\n[6] ASEAN_MASTER_CLEANED.csv")
    master = load_csv("ASEAN_Master_Cleaned.csv")
    print(f"  Total rows: {len(master)}")
    # Check if master has rows with empty Value  
    master_null = sum(1 for r in master if not r["Value"] or r["Value"].strip() == "")
    print(f"  Rows with empty/null Value: {master_null} ({master_null/len(master)*100:.1f}%)")
    # Unique countries in master
    master_countries = {r["CountryCode"] for r in master}
    print(f"  CountryCodes in master: {sorted(master_countries)}")
    # Domain distribution
    master_domains = collections.Counter(r["Domain"] for r in master)
    print(f"  Domain distribution:")
    for d, c in sorted(master_domains.items()):
        print(f"    {d}: {c} rows")

    # ── 7. CROSS-TABLE CONSISTENCY ──────────────────────────────────────────
    print("\n[7] CROSS-TABLE CONSISTENCY")
    # Same countries across all fact tables?
    fact_cc_set = {r["CountryCode"] for r in facts}
    tour_cc_set = {r["DestinationCountryCode"] for r in tourism} | {r["OriginCountryCode"] for r in tourism}
    dim_cc_set = country_codes
    print(f"  Dim_Country codes: {sorted(dim_cc_set)}")
    print(f"  Fact_Indicators codes: {sorted(fact_cc_set)}")
    print(f"  Tourism codes: {sorted(tour_cc_set)}")
    in_dim_not_fact = dim_cc_set - fact_cc_set
    in_fact_not_dim = fact_cc_set - dim_cc_set
    if in_dim_not_fact:
        print(f"  WARN: In Dim_Country but no Fact_Indicators records: {in_dim_not_fact}")
    if in_fact_not_dim:
        print(f"  BUG: In Fact_Indicators but not in Dim_Country: {in_fact_not_dim}")

    print("\n" + "=" * 70)
    print("AUDIT COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    audit()
