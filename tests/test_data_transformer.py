"""
Test Suite: Data Transformer Modular Engines
============================================
Unit tests covering isolated data transformer modules:
- Sanitizer & Type Casting
- Deduplication (Ordered & Tabular)
- Missing Value Imputation (Median & Mode)
- Outlier Detection & Capping (IQR Fences)
- File I/O Safety
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from ai_pair_programming.data_transformer.deduplicator import (
    deduplicate_list,
    deduplicate_tabular_rows,
)
from ai_pair_programming.data_transformer.imputer import (
    calculate_categorical_replacement,
    calculate_numeric_replacement,
    impute_missing_in_matrix,
)
from ai_pair_programming.data_transformer.io_utils import load_csv_file, save_csv_file
from ai_pair_programming.data_transformer.outlier_handler import (
    calculate_quartile_fences,
    cap_matrix_outliers,
)
from ai_pair_programming.data_transformer.sanitizer import (
    infer_and_cast_value,
    is_null_token,
    normalize_date,
    sanitize_currency,
)


class TestDataTransformer(unittest.TestCase):
    """Unit tests for the reusable data_transformer package."""

    def test_null_token_detection(self) -> None:
        """
        Verify identification of missing/null string variants.

        Returns:
            None

        """
        self.assertTrue(is_null_token(None))
        self.assertTrue(is_null_token(""))
        self.assertTrue(is_null_token("N/A"))
        self.assertTrue(is_null_token("null"))
        self.assertTrue(is_null_token("-999"))
        self.assertFalse(is_null_token("Valid String"))
        self.assertFalse(is_null_token(0))

    def test_sanitize_currency(self) -> None:
        """
        Verify multi-currency and accounting negative conversion.

        Returns:
            None

        """
        self.assertEqual(sanitize_currency("$1,200.50"), 1200.50)
        self.assertEqual(sanitize_currency("€500"), 500)
        self.assertEqual(sanitize_currency("£99.99"), 99.99)
        self.assertEqual(sanitize_currency("($150.00)"), -150.00)
        self.assertEqual(sanitize_currency("-$50"), -50)
        self.assertIsNone(sanitize_currency("Not A Currency"))

    def test_normalize_date(self) -> None:
        """
        Verify multiple date formats standardizing to ISO YYYY-MM-DD.

        Returns:
            None

        """
        self.assertEqual(normalize_date("2023/05/20"), "2023-05-20")
        self.assertEqual(normalize_date("15-08-2022"), "2022-08-15")
        self.assertEqual(normalize_date("2023-01-01"), "2023-01-01")
        self.assertIsNone(normalize_date("invalid-date"))

    def test_infer_and_cast_value(self) -> None:
        """
        Verify heuristic data type inference and type casting.

        Returns:
            None

        """
        val, t_name = infer_and_cast_value("$450,000")
        self.assertEqual(val, 450000)
        self.assertEqual(t_name, "int")

        val, t_name = infer_and_cast_value("2023/01/15")
        self.assertEqual(val, "2023-01-15")
        self.assertEqual(t_name, "date")

        val, t_name = infer_and_cast_value("true")
        self.assertEqual(val, True)
        self.assertEqual(t_name, "bool")

        val, t_name = infer_and_cast_value("N/A")
        self.assertIsNone(val)
        self.assertEqual(t_name, "null")

    def test_deduplicate_list(self) -> None:
        """
        Verify order-preserved list deduplication.

        Returns:
            None

        """
        self.assertEqual(deduplicate_list([1, 2, 2, 3, 1]), [1, 2, 3])
        self.assertEqual(deduplicate_list(["a", "b", "a"]), ["a", "b"])
        self.assertEqual(deduplicate_list([]), [])

    def test_deduplicate_tabular_rows(self) -> None:
        """
        Verify tabular matrix deduplication.

        Returns:
            None

        """
        headers = ["id", "val"]
        rows = [["1", "A"], ["2", "B"], ["1", "A"]]
        deduped, count = deduplicate_tabular_rows(headers, rows)
        self.assertEqual(count, 1)
        self.assertEqual(len(deduped), 2)

    def test_imputer_helpers(self) -> None:
        """
        Verify numerical and categorical statistical replacement helpers.

        Returns:
            None

        """
        self.assertEqual(
            calculate_numeric_replacement([10, 20, 30], strategy="median"), 20.0
        )
        self.assertEqual(
            calculate_numeric_replacement([10, 20, 30], strategy="mean"), 20.0
        )
        self.assertEqual(calculate_categorical_replacement(["A", "B", "A"]), "A")

    def test_impute_missing_in_matrix(self) -> None:
        """
        Verify matrix-level missing value imputation.

        Returns:
            None

        """
        headers = ["num", "cat"]
        rows = [[10, "A"], [20, None], [None, "A"]]
        inferred = {"num": "int", "cat": "str"}
        imputed, counts = impute_missing_in_matrix(headers, rows, inferred)
        self.assertEqual(counts["num"], 1)
        self.assertEqual(counts["cat"], 1)
        self.assertEqual(imputed[1][1], "A")
        self.assertEqual(imputed[2][0], 15)

    def test_iqr_outlier_capping(self) -> None:
        """
        Verify IQR bounds computation and Winsorization capping.

        Returns:
            None

        """
        values = [10, 12, 14, 15, 16, 18, 1000]
        bounds = calculate_quartile_fences(values, factor=1.5)
        self.assertIsNotNone(bounds)
        _lower, upper = bounds
        self.assertTrue(upper < 1000)

        headers = ["val"]
        rows = [[10], [12], [14], [15], [16], [18], [1000]]
        inferred = {"val": "int"}
        capped_rows, counts = cap_matrix_outliers(headers, rows, inferred)
        self.assertEqual(counts["val"], 1)
        self.assertTrue(capped_rows[-1][0] < 1000)

    def test_csv_io(self) -> None:
        """
        Verify file saving and reading integrity.

        Returns:
            None

        """
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "test.csv")
            headers = ["col1", "col2"]
            rows = [["1", "a"], ["2", "b"]]
            save_csv_file(file_path, headers, rows)
            self.assertTrue(os.path.exists(file_path))

            loaded_headers, loaded_rows = load_csv_file(file_path)
            self.assertEqual(loaded_headers, headers)
            self.assertEqual(loaded_rows, rows)


if __name__ == "__main__":
    unittest.main(verbosity=2)
