"""
Test Suite: End-to-End Integration & CSV File I/O
===================================================
Tests end-to-end reading, cleaning, audit reporting, and file export.
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from ai_pair_programming.data_cleaner.cleaner_engine import DataCleaningAssistant
from ai_pair_programming.data_cleaner.reporter import generate_audit_report


def _create_sample_dirty_csv(target_path: str) -> None:
    """
    Write a sample dirty CSV file for testing integration pipelines.

    Args:
        target_path (str): Destination filesystem path.

    Returns:
        None

    """
    with open(target_path, "w", encoding="utf-8") as f:
        f.write("id, price, date, category\n")
        f.write("1, $100.00, 2023-01-01, A\n")
        f.write("2, N/A, 2023/02/01, B\n")
        f.write("1, $100.00, 2023-01-01, A\n")


class TestDataCleaningPipelineE2E(unittest.TestCase):
    """Integration test suite executing full workflow from reading to export."""

    def setUp(self) -> None:
        """
        Set up cleaner instance and temporary directory fixture.

        Returns:
            None

        """
        self.assistant = DataCleaningAssistant()
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        """
        Clean up temporary directory fixture.

        Returns:
            None

        """
        self.temp_dir.cleanup()

    def test_e2e_csv_load_clean_export(self) -> None:
        """
        Verify end-to-end load, clean, audit report, and export cycle.

        Returns:
            None

        """
        test_csv = os.path.join(self.temp_dir.name, "raw_data.csv")
        cleaned_csv = os.path.join(self.temp_dir.name, "raw_data_cleaned.csv")

        _create_sample_dirty_csv(test_csv)

        headers, rows = self.assistant.load_csv(test_csv)
        self.assertEqual(len(headers), 4)
        self.assertEqual(len(rows), 3)

        profile = self.assistant.clean_dataset(headers, rows)
        self.assertEqual(profile.metrics.total_rows_initial, 3)
        self.assertEqual(profile.metrics.total_rows_final, 2)
        self.assertEqual(profile.metrics.duplicates_removed, 1)

        report = generate_audit_report(profile, dataset_name="Test Data")
        self.assertIn("DATA QUALITY AUDIT REPORT", report)

        self.assistant.save_csv(cleaned_csv, profile.headers, profile.rows)
        self.assertTrue(os.path.exists(cleaned_csv))

        _loaded_headers, loaded_rows = self.assistant.load_csv(cleaned_csv)
        self.assertEqual(len(loaded_rows), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
