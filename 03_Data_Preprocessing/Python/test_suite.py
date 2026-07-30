import os
import sys
import csv
import math
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLEANED_DIR = os.path.join(BASE_DIR, "02_Data", "Cleaned")

class TestASEANDataPipeline(unittest.TestCase):

    def setUp(self):
        self.fact_path = os.path.join(CLEANED_DIR, "Fact_ASEAN_Indicators.csv")
        self.flow_path = os.path.join(CLEANED_DIR, "Fact_ASEAN_Tourism_Flow.csv")
        self.country_path = os.path.join(CLEANED_DIR, "Dim_Country.csv")
        self.indicator_path = os.path.join(CLEANED_DIR, "Dim_Indicator.csv")
        self.date_path = os.path.join(CLEANED_DIR, "Dim_Date.csv")

    def test_fact_indicators_grain_uniqueness(self):
        """Assert Fact_ASEAN_Indicators has zero duplicate (CountryCode, SeriesCode, Year) composite keys."""
        keys = set()
        duplicates = 0
        with open(self.fact_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row['CountryCode'], row['SeriesCode'], int(row['Year']))
                if key in keys:
                    duplicates += 1
                else:
                    keys.add(key)
        self.assertEqual(duplicates, 0, f"Found {duplicates} duplicate composite keys in Fact_ASEAN_Indicators!")

    def test_tourism_flow_grain_uniqueness(self):
        """Assert Fact_ASEAN_Tourism_Flow has zero duplicate (Destination, Origin, Year) keys."""
        keys = set()
        duplicates = 0
        with open(self.flow_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row['DestinationCountryCode'], row['OriginCountryCode'], int(row['Year']))
                if key in keys:
                    duplicates += 1
                else:
                    keys.add(key)
        self.assertEqual(duplicates, 0, f"Found {duplicates} duplicate keys in Fact_ASEAN_Tourism_Flow!")

    def test_referential_integrity(self):
        """Assert all Fact table foreign keys exist in Dim_Country and Dim_Indicator."""
        countries = set()
        with open(self.country_path, mode='r', encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                countries.add(r['CountryCode'])

        indicators = set()
        with open(self.indicator_path, mode='r', encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                indicators.add(r['SeriesCode'])

        with open(self.fact_path, mode='r', encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                self.assertIn(r['CountryCode'], countries, f"Orphan country code: {r['CountryCode']}")
                self.assertIn(r['SeriesCode'], indicators, f"Orphan indicator code: {r['SeriesCode']}")

    def test_numeric_value_validity(self):
        """Assert all Fact values are valid non-NaN, non-Inf float numbers."""
        with open(self.fact_path, mode='r', encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                val = float(r['Value'])
                self.assertFalse(math.isnan(val))
                self.assertFalse(math.isinf(val))

    def test_dim_date_continuity(self):
        """Assert Dim_Date contains exact 11 continuous years (2015 to 2025)."""
        years = []
        with open(self.date_path, mode='r', encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                years.append(int(r['Year']))
        self.assertEqual(sorted(years), list(range(2015, 2026)))

if __name__ == "__main__":
    unittest.main()
