"""
Data Transformer: Missing Value Imputation Engine
=================================================
Provides statistical imputation strategies:
- Numeric features: Median (resistant to outliers) or Mean
- Categorical features: Mode (most frequent value) or Constant fallback
"""

from __future__ import annotations

import statistics
from typing import Any

from ai_pair_programming.telemetry import get_logger

_LOGGER = get_logger("data_transformer.imputer")


def calculate_numeric_replacement(
    values: list[float | int], strategy: str = "median"
) -> float | int:
    """
    Calculate statistical replacement for continuous numeric series.

    Args:
        values (list[float | int]): Observed numeric sample values.
        strategy (str): Imputation strategy ('median' or 'mean').

    Returns:
        float | int: Calculated central tendency value.

    """
    numeric_vals = [float(v) for v in values if isinstance(v, (int, float))]
    if not numeric_vals:
        return 0

    if strategy == "mean":
        return statistics.mean(numeric_vals)
    return statistics.median(numeric_vals)


def calculate_categorical_replacement(
    values: list[Any], fallback: str = "Unknown"
) -> str:
    """
    Calculate statistical mode for categorical feature series.

    Args:
        values (list[Any]): Observed categorical sample values.
        fallback (str): Fallback string if sample contains no valid values.

    Returns:
        str: Most frequently occurring category or fallback.

    """
    valid_str_vals = [str(v) for v in values if v is not None and str(v).strip() != ""]
    if not valid_str_vals:
        return fallback

    try:
        return statistics.mode(valid_str_vals)
    except statistics.StatisticsError:
        return valid_str_vals[0]


def _calculate_column_replacement(values: list[Any], col_type: str) -> Any:
    """
    Compute median for numeric columns or mode for categorical columns.

    Args:
        values (list[Any]): Non-null values observed in the column.
        col_type (str): Inferred column data type name.

    Returns:
        Any: Computed replacement value matching column type.

    """
    if not values:
        return 0 if col_type in ("int", "float") else "N/A"

    if col_type in ("int", "float"):
        med = calculate_numeric_replacement(values, strategy="median")
        return round(med) if col_type == "int" else round(med, 2)
    return calculate_categorical_replacement(values)


def _build_column_replacements(
    headers: list[str],
    rows: list[list[Any]],
    inferred_types: dict[str, str],
) -> dict[int, Any]:
    """
    Precompute imputation values for each column index.

    Args:
        headers (list[str]): Header column names.
        rows (list[list[Any]]): Tabular data matrix.
        inferred_types (dict[str, str]): Inferred column types dictionary.

    Returns:
        dict[int, Any]: Mapping of column index to replacement value.

    """
    replacements: dict[int, Any] = {}
    for idx, h in enumerate(headers):
        col_type = inferred_types.get(h, "str")
        values = [row[idx] for row in rows if idx < len(row) and row[idx] is not None]
        replacements[idx] = _calculate_column_replacement(values, col_type)
    return replacements


def impute_missing_in_matrix(
    headers: list[str],
    rows: list[list[Any]],
    inferred_types: dict[str, str],
) -> tuple[list[list[Any]], dict[str, int]]:
    """
    Impute null and missing values across all matrix columns.

    Args:
        headers (list[str]): Column headers.
        rows (list[list[Any]]): Tabular 2D data rows.
        inferred_types (dict[str, str]): Inferred types by column name.

    Returns:
        tuple[list[list[Any]], dict[str, int]]: (imputed_rows,
            imputed_counts_by_col).

    """
    if not rows:
        return [], {}

    imputed_counts: dict[str, int] = dict.fromkeys(headers, 0)
    replacements = _build_column_replacements(headers, rows, inferred_types)

    for row in rows:
        for idx in range(len(headers)):
            if idx >= len(row) or row[idx] is None:
                if idx < len(row):
                    row[idx] = replacements[idx]
                else:
                    row.append(replacements[idx])
                imputed_counts[headers[idx]] += 1

    return rows, imputed_counts
