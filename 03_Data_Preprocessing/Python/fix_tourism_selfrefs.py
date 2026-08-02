"""
FIX Script: Remove 9 self-referential rows from Fact_ASEAN_Tourism_Flow.csv
(rows where DestinationCountryCode == OriginCountryCode)
"""
import csv
import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLEANED = os.path.join(BASE, "02_Data", "Cleaned")
tourism_path = os.path.join(CLEANED, "Fact_ASEAN_Tourism_Flow.csv")

with open(tourism_path, encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

before = len(rows)
clean_rows = [r for r in rows if r["DestinationCountryCode"] != r["OriginCountryCode"]]
removed = before - len(clean_rows)

with open(tourism_path, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["DestinationCountryCode", "OriginCountryCode", "Year", "Visitors"])
    writer.writeheader()
    writer.writerows(clean_rows)

print(f"[FIXED] Removed {removed} self-referential rows from Fact_ASEAN_Tourism_Flow.csv")
print(f"  Before: {before} rows -> After: {len(clean_rows)} rows")
