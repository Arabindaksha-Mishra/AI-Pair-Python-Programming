"""
Part 2: Capstone Project — AI-Powered Data Quality Package (Python 3.12+)
========================================================================
Implements Task 2: Automated Data Cleaning Assistant:
- Ingestion of arbitrary tabular datasets (CSV / Matrix)
- Type inference, currency parsing & ISO 8601 date normalization
- Null token standardization (15+ missing representations -> None)
- Order-preserved deduplication
- Robust statistical imputation (mean, median, mode)
- Outlier detection & Winsorization capping via Tukey's IQR Fences
- 1-Hour rotating telemetry logging & formatted audit reporting

100% Pure Standard Library (Zero External Dependencies).
"""

from __future__ import annotations

from .cleaner_engine import (
    CleaningMetrics,
    DataCleaningAssistant,
    DatasetProfile,
)
from .reporter import generate_audit_report

__all__ = [
    "CleaningMetrics",
    "DataCleaningAssistant",
    "DatasetProfile",
    "generate_audit_report",
]
