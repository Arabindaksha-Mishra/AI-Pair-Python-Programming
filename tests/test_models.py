"""
Test Suite: Enterprise Data Models (models.py)
==============================================
Unit tests covering TabularDataset, CleaningConfig, and ReleaseRecord.
"""

from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from ai_pair_programming.models import (
    CleaningConfig,
    ReleaseRecord,
    TabularDataset,
)


class TestDataModels(unittest.TestCase):
    """Unit tests for Capstone & System data models."""

    def test_tabular_dataset(self) -> None:
        """Verify TabularDataset dataclass shape and properties."""
        headers = ["id", "name", "score"]
        rows = [[1, "Alice", 95.5], [2, "Bob", 88.0]]
        dataset = TabularDataset(headers=headers, rows=rows, dataset_name="TestSet")

        self.assertEqual(dataset.num_rows, 2)
        self.assertEqual(dataset.num_cols, 3)
        self.assertEqual(dataset.shape, (2, 3))
        self.assertEqual(dataset.dataset_name, "TestSet")

    def test_cleaning_config_defaults(self) -> None:
        """Verify CleaningConfig default values."""
        cfg = CleaningConfig()
        self.assertEqual(cfg.iqr_factor, 1.5)
        self.assertEqual(cfg.z_score_threshold, 3.0)
        self.assertEqual(cfg.numeric_impute_strategy, "median")
        self.assertEqual(cfg.categorical_impute_strategy, "mode")

    def test_release_record_serialization(self) -> None:
        """Verify ReleaseRecord dataclass serialization to dict."""
        record = ReleaseRecord(
            version=2.0,
            component="DataModels",
            description="Added core enterprise data models.",
            category="Architecture",
        )
        d = record.to_dict()
        self.assertEqual(d["version"], 2.0)
        self.assertEqual(d["component"], "DataModels")
        self.assertEqual(d["category"], "Architecture")
        self.assertTrue(d["is_new"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
