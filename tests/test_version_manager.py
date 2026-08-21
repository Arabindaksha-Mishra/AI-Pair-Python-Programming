"""
Test Suite: Version Manager & Release Notes Engine (release_notes.json)
=============================================================
Unit tests covering schema loading, version extraction, record addition,
and history formatting.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from ai_pair_programming.tools.version_manager import VersionManager


class TestVersionManager(unittest.TestCase):
    """Unit tests for VersionManager and release_notes.json tracking."""

    def setUp(self) -> None:
        """
        Set up temporary sandbox directory fixture with mock release_notes.json.

        Returns:
            None

        """
        self.temp_dir = tempfile.TemporaryDirectory()
        self.rn_path = os.path.join(self.temp_dir.name, "release_notes.json")

        initial_data = [
            {
                "category": "Algorithms",
                "component": "SeniorAlgorithms",
                "description": "Initial Implementation of Senior Algorithms.",
                "epoch_timestamp": 1740528000,
                "is_breaking": False,
                "is_deleted": False,
                "is_new": True,
                "version": 1.0,
            }
        ]
        with open(self.rn_path, "w", encoding="utf-8") as f:
            json.dump(initial_data, f)

        self.vm = VersionManager(rn_file_path=self.rn_path)

    def tearDown(self) -> None:
        """
        Clean up temporary sandbox fixture.

        Returns:
            None

        """
        self.temp_dir.cleanup()

    def test_get_current_version(self) -> None:
        """
        Verify retrieval of current active version.

        Returns:
            None

        """
        self.assertEqual(self.vm.get_current_version(), 1.0)

    def test_add_change_record(self) -> None:
        """
        Verify recording a new version change record in release_notes.json.

        Returns:
            None

        """
        record = self.vm.add_change_record(
            component="OutputHandler",
            description="Added OutputHandler structured logging.",
            category="Module",
            version=2.0,
            is_new=True,
        )

        self.assertEqual(self.vm.get_current_version(), 2.0)
        self.assertEqual(record["component"], "OutputHandler")
        self.assertEqual(record["version"], 2.0)

        with open(self.rn_path, encoding="utf-8") as f:
            persisted = json.load(f)
        self.assertEqual(len(persisted), 2)
        self.assertEqual(persisted[1]["component"], "OutputHandler")

    def test_format_history(self) -> None:
        """
        Verify terminal release notes history output formatting.

        Returns:
            None

        """
        history_text = self.vm.format_history()
        self.assertIn("PROJECT RELEASE NOTES", history_text)
        self.assertIn("Version 1.0", history_text)
        self.assertIn("SeniorAlgorithms", history_text)

    def test_missing_file_fallback(self) -> None:
        """
        Verify graceful fallback when release_notes.json does not exist.

        Returns:
            None

        """
        non_existent_path = os.path.join(self.temp_dir.name, "missing_rn.json")
        vm_fallback = VersionManager(rn_file_path=non_existent_path)
        self.assertEqual(vm_fallback.get_current_version(), 1.0)
        self.assertEqual(len(vm_fallback.get_records()), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
