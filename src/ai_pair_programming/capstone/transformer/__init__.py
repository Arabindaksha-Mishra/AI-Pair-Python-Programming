"""
Data Transformer Package
========================
Reusable, production-grade modular engines for data sanitization, deduplication,
missing value imputation, IQR outlier capping, and robust file I/O.
"""

from .deduplicator import deduplicate_list, deduplicate_tabular_rows
from .imputer import (
    calculate_categorical_replacement,
    calculate_numeric_replacement,
    impute_missing_in_matrix,
)
from .io_utils import load_csv_file, save_csv_file
from .outlier_handler import calculate_quartile_fences, cap_matrix_outliers
from .sanitizer import (
    NULL_STRINGS,
    infer_and_cast_value,
    is_null_token,
    normalize_date,
    sanitize_currency,
    sanitize_text,
)

__all__ = [
    "NULL_STRINGS",
    "calculate_categorical_replacement",
    "calculate_numeric_replacement",
    "calculate_quartile_fences",
    "cap_matrix_outliers",
    "deduplicate_list",
    "deduplicate_tabular_rows",
    "impute_missing_in_matrix",
    "infer_and_cast_value",
    "is_null_token",
    "load_csv_file",
    "normalize_date",
    "sanitize_currency",
    "sanitize_text",
    "save_csv_file",
]
