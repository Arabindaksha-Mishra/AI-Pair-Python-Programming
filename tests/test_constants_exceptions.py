"""
Test Suite: Constants & Exception Hierarchy (constants.py & exceptions.py)
==========================================================================
Unit tests covering project constants, default parameters, and custom exceptions.
"""

from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from ai_pair_programming.constants import (
    DEFAULT_IQR_FACTOR,
    DEFAULT_Z_SCORE_THRESHOLD,
    MAX_LINE_LENGTH,
    NULL_STRINGS,
    SUPPORTED_DATE_FORMATS,
)
from ai_pair_programming.exceptions import (
    AIPairProgrammingError,
    ColumnNotFoundError,
    DataCleanerError,
    DatasetValidationError,
    FileProcessingError,
    ReleaseNotesSchemaError,
    VersionManagerError,
)


class TestConstantsAndExceptions(unittest.TestCase):
    """Unit tests for constants and custom exception classes."""

    def test_constants_values(self) -> None:
        """Verify default constant values and null string sets."""
        self.assertEqual(DEFAULT_IQR_FACTOR, 1.5)
        self.assertEqual(DEFAULT_Z_SCORE_THRESHOLD, 3.0)
        self.assertEqual(MAX_LINE_LENGTH, 88)
        self.assertIn("null", NULL_STRINGS)
        self.assertIn("missing", NULL_STRINGS)
        self.assertIn("%Y-%m-%d", SUPPORTED_DATE_FORMATS)

    def test_exception_inheritance_hierarchy(self) -> None:
        """Verify exception inheritance chain."""
        self.assertTrue(issubclass(DataCleanerError, AIPairProgrammingError))
        self.assertTrue(issubclass(DatasetValidationError, DataCleanerError))
        self.assertTrue(issubclass(ColumnNotFoundError, DataCleanerError))
        self.assertTrue(issubclass(FileProcessingError, DataCleanerError))
        self.assertTrue(issubclass(VersionManagerError, AIPairProgrammingError))
        self.assertTrue(issubclass(ReleaseNotesSchemaError, VersionManagerError))

    def test_raising_custom_exception(self) -> None:
        """Verify custom exception raising behavior."""
        with self.assertRaises(DatasetValidationError) as ctx:
            raise DatasetValidationError("Empty dataset matrix provided.")
        self.assertIn("Empty dataset matrix", str(ctx.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
