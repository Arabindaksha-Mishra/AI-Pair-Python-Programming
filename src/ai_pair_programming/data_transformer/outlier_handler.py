"""
Data Transformer: Statistical Outlier & Anomaly Handler
========================================================
Implements Interquartile Range (IQR) fence calculations and Winsorization (capping).
Bounds anomalies to [Q1 - 1.5 * IQR, Q3 + 1.5 * IQR].
"""

from __future__ import annotations

import math
from typing import Any

from ai_pair_programming.telemetry import get_logger

_LOGGER = get_logger("data_transformer.outlier_handler")


def _calculate_quartiles(nums: list[float]) -> tuple[float, float]:
    """
    Calculate Q1 (25th percentile) and Q3 (75th percentile) from sorted sample.

    Args:
        nums (list[float]): Sorted numeric sample values.

    Returns:
        tuple[float, float]: (q1_value, q3_value).

    """
    n = len(nums)
    q1_idx = math.floor(0.25 * (n - 1))
    q3_idx = math.ceil(0.75 * (n - 1))
    return nums[q1_idx], nums[q3_idx]


def calculate_quartile_fences(
    values: list[float | int], factor: float = 1.5
) -> tuple[float, float] | None:
    """
    Calculate Lower and Upper outlier boundaries using the IQR rule.

    Args:
        values (list[float | int]): Observed numeric sample values.
        factor (float): IQR multiplier for fence threshold (default: 1.5).

    Returns:
        tuple[float, float] | None: (lower_fence, upper_fence) or None if sample
            size is under 4 or IQR is 0.

    """
    nums = sorted(float(v) for v in values if isinstance(v, (int, float)))
    if len(nums) < 4:
        return None

    q1, q3 = _calculate_quartiles(nums)
    iqr = q3 - q1

    if iqr == 0:
        return None

    lower_fence = q1 - (factor * iqr)
    upper_fence = q3 + (factor * iqr)
    return lower_fence, upper_fence


def _cap_value(val: float, lower: float, upper: float, col_type: str) -> float | int:
    """
    Clamp value within [lower, upper] boundaries preserving precision.

    Args:
        val (float): Numeric value to clamp.
        lower (float): Lower fence threshold.
        upper (float): Upper fence threshold.
        col_type (str): Target column data type ('int' or 'float').

    Returns:
        float | int: Clamped and rounded value.

    """
    clamped = max(lower, min(upper, val))
    return round(clamped) if col_type == "int" else round(clamped, 2)


def cap_matrix_outliers(
    headers: list[str],
    rows: list[list[Any]],
    inferred_types: dict[str, str],
    iqr_factor: float = 1.5,
) -> tuple[list[list[Any]], dict[str, int]]:
    """
    Detect numeric outliers using IQR fences and cap them via Winsorization.

    Args:
        headers (list[str]): Column header names.
        rows (list[list[Any]]): Tabular 2D data rows.
        inferred_types (dict[str, str]): Inferred column types dictionary.
        iqr_factor (float): Multiplier for IQR fence calculation.

    Returns:
        tuple[list[list[Any]], dict[str, int]]: (capped_rows,
            outlier_counts_by_column).

    """
    if not rows:
        return [], {}

    outlier_counts: dict[str, int] = dict.fromkeys(headers, 0)

    for idx, h in enumerate(headers):
        col_type = inferred_types.get(h, "str")
        if col_type not in ("int", "float"):
            continue

        col_values = [
            float(row[idx])
            for row in rows
            if idx < len(row) and isinstance(row[idx], (int, float))
        ]

        bounds = calculate_quartile_fences(col_values, factor=iqr_factor)
        if bounds is None:
            continue

        lower_fence, upper_fence = bounds

        for row in rows:
            if idx < len(row) and isinstance(row[idx], (int, float)):
                val = float(row[idx])
                if val < lower_fence or val > upper_fence:
                    outlier_counts[h] += 1
                    row[idx] = _cap_value(val, lower_fence, upper_fence, col_type)

    return rows, outlier_counts
