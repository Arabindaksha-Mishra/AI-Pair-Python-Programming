"""
Test Suite: Task 2 — Automated Data Cleaning Assistant
========================================================
Unit tests covering schema inference, currency cleaning, missing value imputation,
outlier bounds, duplicate elimination, and custom trainer datasets.
"""

import unittest
import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from capstone.data_cleaner.cleaner_engine import DataCleaningAssistant


class TestDataCleaningAssistant(unittest.TestCase):
    """Unit tests for Task 2: Automated Data Cleaning Assistant."""

    def setUp(self):
        self.cleaner = DataCleaningAssistant()

    def test_type_sanitization(self):
        self.assertEqual(self.cleaner.sanitize_value("$450,000"), 450000)
        self.assertEqual(self.cleaner.sanitize_value("-$50.50"), -50.5)
        self.assertEqual(self.cleaner.sanitize_value("N/A"), None)
        self.assertEqual(self.cleaner.sanitize_value("2023/01/15"), "2023-01-15")

    def test_duplicate_removal(self):
        headers = ["id", "val"]
        rows = [["1", "A"], ["2", "B"], ["1", "A"]]
        deduped, count = self.cleaner.remove_duplicates(headers, rows)
        self.assertEqual(count, 1)
        self.assertEqual(len(deduped), 2)

    def test_custom_trainer_dataset_scenario(self):
        """Tests arbitrary schema with messy strings, currency, jagged rows, outliers, and duplicates."""
        headers = ["emp_id", "department", "salary", "bonus_pct", "start_date"]
        raw_rows = [
            ["E101", "Engineering", "$120,000", "15.5", "2021-05-10"],
            ["E102", "Marketing", "$85,000", "10.0", "10-06-2020"],
            ["E103", "Engineering", "null", "12.0", "2019/03/15"],  # Missing salary
            ["E104", "Sales", "$75,000", "N/A", "2022-01-01"],     # Missing bonus
            ["E105", "Executive", "$9,999,999", "50.0", "2015-11-20"],  # Outlier salary
            ["E101", "Engineering", "$120,000", "15.5", "2021-05-10"],  # Exact duplicate
            ["E106", "Sales", "$70,000"],  # Jagged row (fewer columns)
        ]
        profile = self.cleaner.clean_dataset(headers, raw_rows)

        # 1. Duplicate should be removed (7 -> 6 unique rows)
        self.assertEqual(profile.metrics.duplicates_removed, 1)
        self.assertEqual(len(profile.rows), 6)

        # 2. Inferred types
        self.assertEqual(profile.inferred_types["salary"], "int")
        self.assertEqual(profile.inferred_types["department"], "str")

        # 3. Missing values imputed
        self.assertGreaterEqual(profile.metrics.missing_values_imputed["salary"], 1)

        # 4. Outlier capped
        self.assertGreaterEqual(profile.metrics.outliers_detected["salary"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
