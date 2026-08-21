"""
Data Cleaning Assistant Engine
==============================
High-level orchestration engine composed using the reusable `data_transformer` package.

Core Capabilities:
1. Automated Missing Value Detection & Statistical Imputation (Median / Mode)
2. Statistical Outlier Detection & Handling (IQR Fences & Winsorization)
3. Heuristic Data Type Inference & String/Currency Sanitization
4. Exact & Key-Based Duplicate Detection and Removal
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ai_pair_programming.data_transformer.deduplicator import (
    deduplicate_tabular_rows,
)
from ai_pair_programming.data_transformer.imputer import impute_missing_in_matrix
from ai_pair_programming.data_transformer.io_utils import (
    load_csv_file,
    save_csv_file,
)
from ai_pair_programming.data_transformer.outlier_handler import cap_matrix_outliers
from ai_pair_programming.data_transformer.sanitizer import infer_and_cast_value
from ai_pair_programming.models import PrimitiveValue, RawCellValue
from ai_pair_programming.telemetry import OutputHandler, get_logger


@dataclass(slots=True)
class CleaningMetrics:
    """Stores quantitative audit metrics gathered during dataset cleaning."""

    total_rows_initial: int = 0
    total_rows_final: int = 0
    duplicates_removed: int = 0
    missing_values_imputed: dict[str, int] = field(default_factory=dict)
    outliers_detected: dict[str, int] = field(default_factory=dict)
    type_corrections_applied: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class DatasetProfile:
    """Holds cleaned dataset matrix, schema types, and quantitative metrics."""

    headers: list[str]
    rows: list[list[Any]]
    inferred_types: dict[str, str]
    metrics: CleaningMetrics


class DataCleaningAssistant:
    """Production-grade tabular data cleaner composed via modular transformers."""

    def __init__(
        self,
        iqr_factor: float = 1.5,
        z_score_threshold: float = 3.0,
        logger: OutputHandler | None = None,
    ) -> None:
        """
        Initialize the Data Cleaning Assistant engine.

        Args:
            iqr_factor (float): Multiplier for IQR outlier fences (default: 1.5).
            z_score_threshold (float): Z-score threshold for parametric checks.
            logger (OutputHandler | None): Structured logger instance.

        Returns:
            None

        """
        self.iqr_factor = iqr_factor
        self.z_score_threshold = z_score_threshold
        self.logger = logger or get_logger("data_cleaner")

    def load_csv(self, file_path: str) -> tuple[list[str], list[list[str]]]:
        """
        Load a CSV file and trim outer whitespace from cells.

        Args:
            file_path (str): Filesystem path to the CSV file.

        Returns:
            tuple[list[str], list[list[str]]]: (headers, rows) tuple.

        """
        self.logger.debug(f"Loading CSV file: {file_path}")
        return load_csv_file(file_path)

    def save_csv(
        self, file_path: str, headers: list[str], rows: list[list[Any]]
    ) -> None:
        """
        Export tabular data matrix to a CSV file.

        Args:
            file_path (str): Destination CSV filepath.
            headers (list[str]): Header row columns.
            rows (list[list[Any]]): 2D matrix rows to export.

        Returns:
            None

        """
        self.logger.info(f"Saving cleaned dataset to: {file_path}")
        save_csv_file(file_path, headers, rows)

    def sanitize_value(self, val: RawCellValue) -> PrimitiveValue:
        """Sanitize raw string values into typed native representations."""
        casted_val, _ = infer_and_cast_value(val)
        return casted_val

    def _count_column_types(
        self, col_idx: int, rows: list[list[Any]]
    ) -> dict[str, int]:
        """
        Count non-null inferred types in a specific column index.

        Args:
            col_idx (int): Column index in tabular matrix.
            rows (list[list[Any]]): Tabular 2D data rows.

        Returns:
            dict[str, int]: Mapping of type names to occurrence counts.

        """
        type_counts: dict[str, int] = {}
        for row in rows:
            if col_idx < len(row) and row[col_idx] is not None:
                _, t_name = infer_and_cast_value(row[col_idx])
                if t_name != "null":
                    type_counts[t_name] = type_counts.get(t_name, 0) + 1
        return type_counts

    def infer_column_types(
        self, headers: list[str], rows: list[list[Any]]
    ) -> dict[str, str]:
        """
        Infer majority native data type for each column header.

        Args:
            headers (list[str]): List of column names.
            rows (list[list[Any]]): Tabular data matrix.

        Returns:
            dict[str, str]: Mapping of header name to inferred type.

        """
        inferred: dict[str, str] = {}
        for idx, h in enumerate(headers):
            type_counts = self._count_column_types(idx, rows)
            inferred[h] = (
                max(type_counts, key=type_counts.get) if type_counts else "str"
            )
        self.logger.debug(f"Inferred column schemas: {inferred}")
        return inferred

    def remove_duplicates(
        self,
        headers: list[str],
        rows: list[list[Any]],
        key_column: str | None = None,
    ) -> tuple[list[list[Any]], int]:
        """
        Remove duplicate rows based on all columns or a primary key.

        Args:
            headers (list[str]): Column header names.
            rows (list[list[Any]]): Tabular data rows.
            key_column (str | None): Optional primary key column name.

        Returns:
            tuple[list[list[Any]], int]: (deduplicated_rows, count_removed).

        """
        deduped, count = deduplicate_tabular_rows(headers, rows, key_column=key_column)
        if count > 0:
            self.logger.info(f"Deduplication removed {count} duplicate rows.")
        return deduped, count

    def impute_missing_values(
        self,
        headers: list[str],
        rows: list[list[Any]],
        inferred_types: dict[str, str],
    ) -> tuple[list[list[Any]], dict[str, int]]:
        """
        Impute missing values using median for numeric or mode for categorical.

        Args:
            headers (list[str]): Column headers.
            rows (list[list[Any]]): Tabular data rows.
            inferred_types (dict[str, str]): Column types dictionary.

        Returns:
            tuple[list[list[Any]], dict[str, int]]: (imputed_rows,
                imputed_counts_by_col).

        """
        imputed_rows, counts = impute_missing_in_matrix(headers, rows, inferred_types)
        total_imputed = sum(counts.values())
        if total_imputed > 0:
            self.logger.info(
                f"Missing value imputation filled {total_imputed} null entries."
            )
        return imputed_rows, counts

    def handle_outliers(
        self,
        headers: list[str],
        rows: list[list[Any]],
        inferred_types: dict[str, str],
    ) -> tuple[list[list[Any]], dict[str, int]]:
        """
        Detect numeric anomalies and cap them using IQR fences.

        Args:
            headers (list[str]): Column headers.
            rows (list[list[Any]]): Tabular data rows.
            inferred_types (dict[str, str]): Column types dictionary.

        Returns:
            tuple[list[list[Any]], dict[str, int]]: (capped_rows,
                outlier_counts_by_col).

        """
        capped_rows, counts = cap_matrix_outliers(
            headers, rows, inferred_types, iqr_factor=self.iqr_factor
        )
        total_outliers = sum(counts.values())
        if total_outliers > 0:
            self.logger.info(
                f"Winsorization capped {total_outliers} statistical outliers."
            )
        return capped_rows, counts

    def _sanitize_rows(self, raw_rows: list[list[str]]) -> list[list[Any]]:
        """
        Apply type casting and null normalization across raw rows.

        Args:
            raw_rows (list[list[str]]): Raw string matrix rows.

        Returns:
            list[list[Any]]: Sanitized and type-cast matrix rows.

        """
        return [[self.sanitize_value(cell) for cell in row] for row in raw_rows]

    def clean_dataset(
        self,
        raw_headers: list[str],
        raw_rows: list[list[str]],
        key_column: str | None = None,
    ) -> DatasetProfile:
        """
        Execute full end-to-end dataset cleaning pipeline.

        Args:
            raw_headers (list[str]): Header names of the raw dataset.
            raw_rows (list[list[str]]): Raw data rows.
            key_column (str | None): Optional primary key column name.

        Returns:
            DatasetProfile: Completed dataset profile containing cleaned matrix,
                schema types, and quantitative cleaning metrics.

        """
        self.logger.info(f"Initiating dataset cleaning for {len(raw_rows)} records...")
        metrics = CleaningMetrics()
        metrics.total_rows_initial = len(raw_rows)

        sanitized_rows = self._sanitize_rows(raw_rows)
        inferred_types = self.infer_column_types(raw_headers, sanitized_rows)
        metrics.type_corrections_applied = inferred_types

        deduped_rows, dups_removed = self.remove_duplicates(
            raw_headers, sanitized_rows, key_column=key_column
        )
        metrics.duplicates_removed = dups_removed
        self.logger.log_transformation_step(
            "Deduplication", len(sanitized_rows), len(deduped_rows)
        )

        imputed_rows, imputed_counts = self.impute_missing_values(
            raw_headers, deduped_rows, inferred_types
        )
        metrics.missing_values_imputed = imputed_counts

        final_rows, outlier_counts = self.handle_outliers(
            raw_headers, imputed_rows, inferred_types
        )
        metrics.outliers_detected = outlier_counts
        metrics.total_rows_final = len(final_rows)

        self.logger.info(
            f"Dataset cleaning completed: {len(final_rows)} records ready."
        )

        return DatasetProfile(
            headers=raw_headers,
            rows=final_rows,
            inferred_types=inferred_types,
            metrics=metrics,
        )
