"""
Data Quality Audit Report Generator
====================================
Produces human-readable terminal dashboards and markdown audit summaries.
"""

from __future__ import annotations

from typing import Any

from .cleaner_engine import CleaningMetrics, DatasetProfile


def _calculate_health_score(m: CleaningMetrics) -> float:
    """
    Calculate heuristic data health score percentage.

    Args:
        m (CleaningMetrics): Cleaning metrics container.

    Returns:
        float: Percentage score bounded within [0.0, 100.0].

    """
    if m.total_rows_initial == 0:
        return 100.0
    issues = (
        m.duplicates_removed
        + sum(m.missing_values_imputed.values())
        + sum(m.outliers_detected.values())
    )
    score = 100.0 - (issues / (m.total_rows_initial * 3) * 100.0)
    return max(0.0, min(100.0, score))


def _compute_column_widths(headers: list[str], rows: list[list[Any]]) -> list[int]:
    """
    Calculate maximum character width per column across headers and rows.

    Args:
        headers (list[str]): Header column names.
        rows (list[list[Any]]): Tabular 2D data rows.

    Returns:
        list[int]: List of integer column widths.

    """
    num_cols = len(headers)
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i in range(num_cols):
            val = row[i] if i < len(row) else ""
            widths[i] = max(widths[i], len(str(val)))
    return widths


def _format_table_row(row: list[Any], widths: list[int], num_cols: int) -> str:
    """
    Format a single row with padded column spacing.

    Args:
        row (list[Any]): Data row cells.
        widths (list[int]): Target column widths.
        num_cols (int): Number of columns.

    Returns:
        str: Padded, pipe-delimited row string.

    """
    formatted_cells = [
        f"{row[i] if i < len(row) else ''!s:{widths[i]}}" for i in range(num_cols)
    ]
    return " | ".join(formatted_cells)


def _format_ascii_table(headers: list[str], rows: list[list[Any]]) -> str:
    """
    Format 2D matrix into an ASCII table with column width handling.

    Args:
        headers (list[str]): Table column headers.
        rows (list[list[Any]]): 2D matrix rows.

    Returns:
        str: Rendered ASCII grid table.

    """
    if not headers or not rows:
        return "(Empty Table)"

    num_cols = len(headers)
    widths = _compute_column_widths(headers, rows)

    header_line = " | ".join(f"{h!s:{widths[i]}}" for i, h in enumerate(headers))
    separator = "-+-".join("-" * widths[i] for i in range(num_cols))
    row_lines = [_format_table_row(r, widths, num_cols) for r in rows]

    return f"{header_line}\n{separator}\n" + "\n".join(row_lines)


def generate_audit_report(
    profile: DatasetProfile, dataset_name: str = "Dataset"
) -> str:
    """
    Generate a formatted Terminal and Markdown data quality audit report.

    Args:
        profile (DatasetProfile): Cleaned dataset profile with metrics.
        dataset_name (str): Display name for the audited dataset.

    Returns:
        str: Multi-line formatted audit report dashboard.

    """
    m = profile.metrics
    lines = [
        "\n=======================================================",
        f"   📊 DATA QUALITY AUDIT REPORT: {dataset_name.upper()}   ",
        "=======================================================",
        f"• Initial Record Count:      {m.total_rows_initial}",
        f"• Cleaned Record Count:      {m.total_rows_final}",
        f"• Duplicate Rows Removed:    {m.duplicates_removed}",
        f"• Net Data Health Score:     {_calculate_health_score(m):.1f}%",
        "\n--- 1. Inferred Data Types ---",
    ]

    for col, col_type in profile.inferred_types.items():
        lines.append(f"  • {col:20s} -> {col_type.upper()}")

    lines.append("\n--- 2. Missing Value Imputations ---")
    missing_total = sum(m.missing_values_imputed.values())
    if missing_total == 0:
        lines.append("  • No missing values detected! (100% complete)")
    else:
        for col, count in m.missing_values_imputed.items():
            if count > 0:
                lines.append(f"  • {col:20s}: {count} values imputed")

    lines.append("\n--- 3. Statistical Outliers Detected & Capped ---")
    outlier_total = sum(m.outliers_detected.values())
    if outlier_total == 0:
        lines.append("  • No statistical outliers detected.")
    else:
        for col, count in m.outliers_detected.items():
            if count > 0:
                lines.append(f"  • {col:20s}: {count} outliers treated via IQR fence")

    lines.append("\n--- 4. Cleaned Data Sample (First 5 Rows) ---")
    lines.append(_format_ascii_table(profile.headers, profile.rows[:5]))
    lines.append("=======================================================\n")

    return "\n".join(lines)
