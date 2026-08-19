"""
Test Suite: Task 2 — Automated Data Cleaning Assistant
========================================================
Unit tests covering schema inference, currency cleaning, missing value imputation,
outlier bounds, duplicate elimination, and custom trainer datasets.
"""

from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from ai_pair_programming.data_cleaner.cleaner_engine import DataCleaningAssistant


class TestDataCleaningAssistant(unittest.TestCase):
    """Unit tests for Task 2: Automated Data Cleaning Assistant."""

    def setUp(self) -> None:
        """
        Set up cleaner instance fixture for testing.

        Returns:
            None

        """
        self.cleaner = DataCleaningAssistant()

    def test_type_sanitization(self) -> None:
        """
        Verify currency, ISO date, and null string sanitization.

        Returns:
            None

        """
        self.assertEqual(self.cleaner.sanitize_value("$450,000"), 450000)
        self.assertEqual(self.cleaner.sanitize_value("-$50.50"), -50.5)
        self.assertIsNone(self.cleaner.sanitize_value("N/A"))
        self.assertEqual(self.cleaner.sanitize_value("2023/01/15"), "2023-01-15")

    def test_duplicate_removal(self) -> None:
        """
        Verify removal of duplicate matrix rows.

        Returns:
            None

        """
        headers = ["id", "name", "price"]
        rows = [
            ["1", "Item A", "100"],
            ["2", "Item B", "200"],
            ["1", "Item A", "100"],
        ]
        deduped, count = self.cleaner.remove_duplicates(headers, rows)
        self.assertEqual(count, 1)
        self.assertEqual(len(deduped), 2)
        self.assertEqual(deduped[0][0], "1")
        self.assertEqual(deduped[1][0], "2")

    def test_custom_trainer_dataset_scenario(self) -> None:
        """
        Test arbitrary schema with messy strings, currency, and outliers.

        Returns:
            None

        """
        headers = ["emp_id", "name", "salary", "bonus_pct", "start_date"]
        raw_rows = [
            ["E101", "Alice", "$75,000", "10%", "2022-01-10"],
            ["E102", "Bob", "$82,000", "12%", "2022/03/15"],
            ["E103", "Charlie", "N/A", "null", "15-05-2022"],
            ["E104", "Diana", "$999,999,999", "15%", "2022-06-01"],
            ["E101", "Alice", "$75,000", "10%", "2022-01-10"],
            ["E105", "Evan", "$68,000"],
        ]

        profile = self.cleaner.clean_dataset(headers, raw_rows)

        self.assertEqual(profile.metrics.total_rows_initial, 6)
        self.assertEqual(profile.metrics.total_rows_final, 5)
        self.assertEqual(profile.metrics.duplicates_removed, 1)
        self.assertIn("salary", profile.inferred_types)
        self.assertEqual(profile.inferred_types["salary"], "int")
        salaries = [row[2] for row in profile.rows]
        self.assertTrue(all(s < 100000000 for s in salaries))


if __name__ == "__main__":
    unittest.main(verbosity=2)
