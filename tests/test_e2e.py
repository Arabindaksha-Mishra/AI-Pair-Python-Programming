"""
Test Suite: End-to-End Integration & CSV File I/O
===================================================
Tests end-to-end reading, cleaning, audit report formatting, and export to destination files.
"""

import os
import sys
import tempfile
import unittest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from capstone.data_cleaner.cleaner_engine import DataCleaningAssistant
from capstone.data_cleaner.reporter import generate_audit_report


class TestDataCleaningPipelineE2E(unittest.TestCase):
    """Integration test suite executing full workflow from file reading to export."""

    def setUp(self):
        self.assistant = DataCleaningAssistant()
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_e2e_csv_load_clean_export(self):
        test_csv = os.path.join(self.temp_dir.name, "raw_data.csv")
        cleaned_csv = os.path.join(self.temp_dir.name, "cleaned_data.csv")

        # Create raw sample file
        with open(test_csv, "w", encoding="utf-8") as f:
            f.write("user_id,revenue,signup_date\n")
            f.write("1001,$500,2023-01-01\n")
            f.write("1002,N/A,2023/02/01\n")
            f.write("1003,$1000000,2023-03-01\n")  # Outlier
            f.write("1001,$500,2023-01-01\n")  # Duplicate

        headers, raw_rows = self.assistant.load_csv(test_csv)
        self.assertEqual(len(raw_rows), 4)

        profile = self.assistant.clean_dataset(headers, raw_rows)
        self.assertEqual(len(profile.rows), 3)  # Duplicate removed

        report = generate_audit_report(profile, dataset_name="E2E Test")
        self.assertIn("DATA QUALITY AUDIT REPORT", report)

        self.assistant.save_csv(cleaned_csv, profile.headers, profile.rows)
        self.assertTrue(os.path.isfile(cleaned_csv))


if __name__ == "__main__":
    unittest.main(verbosity=2)
