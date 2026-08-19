"""
Data Quality Audit Report Generator
====================================
Produces human-readable terminal dashboards and markdown audit summaries.
"""

from typing import Any, List
from .cleaner_engine import DatasetProfile


def generate_audit_report(profile: DatasetProfile, dataset_name: str = "Dataset") -> str:
    """Generates a comprehensive Markdown and Terminal audit report."""
    m = profile.metrics
    lines = [
        f"\n=======================================================",
        f"   📊 DATA QUALITY AUDIT REPORT: {dataset_name.upper()}   ",
        f"=======================================================",
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


def _calculate_health_score(m: Any) -> float:
    """Calculates heuristic data health percentage (0 to 100)."""
    if m.total_rows_initial == 0:
        return 100.0
    issues = (
        m.duplicates_removed
        + sum(m.missing_values_imputed.values())
        + sum(m.outliers_detected.values())
    )
    score = 100.0 - (issues / (m.total_rows_initial * 3) * 100.0)
    return max(0.0, min(100.0, score))


def _format_ascii_table(headers: List[str], rows: List[List[Any]]) -> str:
    """Formats 2D matrix into a clean ASCII table."""
    if not rows:
        return "(Empty Table)"

    # Compute column widths
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))

    header_line = " | ".join(f"{str(h):{widths[i]}}" for i, h in enumerate(headers))
    separator = "-+-".join("-" * widths[i] for i in range(len(headers)))

    row_lines = []
    for row in rows:
        row_str = " | ".join(f"{str(val):{widths[i]}}" for i, val in enumerate(row))
        row_lines.append(row_str)

    return f"{header_line}\n{separator}\n" + "\n".join(row_lines)
