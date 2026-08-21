"""
Central Project Constants & Configuration Defaults
===================================================
Defines centralized magic values, default configuration parameters,
regex patterns, and null representations used across the codebase.

100% Pure Standard Library.
"""

from __future__ import annotations

DEFAULT_IQR_FACTOR: float = 1.5
DEFAULT_Z_SCORE_THRESHOLD: float = 3.0
DEFAULT_NUMERIC_IMPUTE_STRATEGY: str = "median"
DEFAULT_CATEGORICAL_IMPUTE_STRATEGY: str = "mode"

NULL_STRINGS: frozenset[str] = frozenset(
    {
        "",
        "n/a",
        "na",
        "null",
        "none",
        "nan",
        "-999",
        "?",
        "nil",
        "undefined",
        "missing",
    }
)

SUPPORTED_DATE_FORMATS: tuple[str, ...] = (
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%Y/%m/%d",
    "%d-%m-%Y",
    "%m-%d-%Y",
)

CURRENCY_REGEX_PATTERN: str = r"[\$,€,£,¥]"
ACCOUNTING_NEGATIVE_PATTERN: str = r"^\(?-?[\d,]+(\.\d+)?\)?$"
ISO_DATE_REGEX_PATTERN: str = r"^\d{2,4}[-/\.]\d{1,2}[-/\.]\d{1,4}$"

MAX_LINE_LENGTH: int = 88
DEFAULT_RELEASE_NOTES_FILE: str = "release_notes.json"
