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
                keys.add(key)
        self.assertEqual(duplicates, 0, f"Found {duplicates} duplicate composite keys in Fact_ASEAN_Indicators!")

    def test_fact_tourism_flow_grain_uniqueness(self):
        """Assert Fact_ASEAN_Tourism_Flow has zero duplicate (DestinationCountryCode, OriginCountryCode, Year) keys."""
        keys = set()
        duplicates = 0
        with open(self.flow_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row['DestinationCountryCode'], row['OriginCountryCode'], int(row['Year']))
                if key in keys:
                    duplicates += 1
                keys.add(key)
        self.assertEqual(duplicates, 0, f"Found {duplicates} duplicate keys in Fact_ASEAN_Tourism_Flow!")

    def test_foreign_key_referential_integrity(self):
        """Assert all CountryCode, SeriesCode, and Year in Fact tables exist in Dim tables."""
        countries = set()
        with open(self.country_path, mode='r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                countries.add(row['CountryCode'])

        indicators = set()
        with open(self.indicator_path, mode='r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                indicators.add(row['SeriesCode'])

        years = set()
        with open(self.date_path, mode='r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                years.add(int(row['Year']))

        with open(self.fact_path, mode='r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                self.assertIn(row['CountryCode'], countries, f"Invalid CountryCode: {row['CountryCode']}")
                self.assertIn(row['SeriesCode'], indicators, f"Invalid SeriesCode: {row['SeriesCode']}")
                self.assertIn(int(row['Year']), years, f"Invalid Year: {row['Year']}")

    def test_no_null_or_nan_in_fact_values(self):
        """Assert no null, blank, or NaN values exist in Fact tables."""
        with open(self.fact_path, mode='r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                val_str = row['Value']
                self.assertIsNotNone(val_str, "Found None in Fact Value!")
                self.assertNotEqual(val_str.strip(), "", "Found blank string in Fact Value!")
                val_float = float(val_str)
                self.assertFalse(math.isnan(val_float), "Found NaN in Fact Value!")

if __name__ == "__main__":
    unittest.main()
