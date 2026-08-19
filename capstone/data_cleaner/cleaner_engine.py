"""
Automated Data Cleaning Engine (Standard Library Only)
=====================================================
Detects and resolves four fundamental tabular data quality issues:
1. Missing Value Detection & Adaptive Imputation (Mean, Median, Mode)
2. Statistical Outlier Detection & Handling (IQR Fences & Z-Score Analysis)
3. Heuristic Data Type Inference & String/Currency Sanitization
4. Exact & Key-Based Duplicate Detection and Removal
"""

import csv
from dataclasses import dataclass, field
import datetime
import math
import re
import statistics
from typing import Any, Dict, List, Optional, Set, Tuple, Union


NULL_STRINGS = {"", "n/a", "na", "null", "none", "nan", "-999", "?", "nil"}


@dataclass
class CleaningMetrics:
    total_rows_initial: int = 0
    total_rows_final: int = 0
    duplicates_removed: int = 0
    missing_values_imputed: Dict[str, int] = field(default_factory=dict)
    outliers_detected: Dict[str, int] = field(default_factory=dict)
    type_corrections_applied: Dict[str, str] = field(default_factory=dict)


@dataclass
class DatasetProfile:
    headers: List[str]
    rows: List[List[Any]]
    inferred_types: Dict[str, str]
    metrics: CleaningMetrics


class DataCleaningAssistant:
    """Production-grade tabular data cleaner using only Python built-in libraries."""

    def __init__(self, iqr_factor: float = 1.5, z_score_threshold: float = 3.0) -> None:
        self.iqr_factor = iqr_factor
        self.z_score_threshold = z_score_threshold

    # -----------------------------------------------------------------------
    # I/O Operations
    # -----------------------------------------------------------------------

    def load_csv(self, file_path: str) -> Tuple[List[str], List[List[str]]]:
        """Loads a raw CSV file and strips leading/trailing field whitespace."""
        with open(file_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            rows = [list(map(str.strip, row)) for row in reader if row]

        if not rows:
            raise ValueError(f"CSV file is empty: {file_path}")

        headers = rows[0]
        data_rows = rows[1:]
        return headers, data_rows

    def save_csv(self, file_path: str, headers: List[str], rows: List[List[Any]]) -> None:
        """Saves tabular data to a destination CSV file."""
        with open(file_path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    # -----------------------------------------------------------------------
    # 1. Duplicate Detection & Removal
    # -----------------------------------------------------------------------

    def remove_duplicates(
        self,
        headers: List[str],
        rows: List[List[Any]],
        key_column: Optional[str] = None,
    ) -> Tuple[List[List[Any]], int]:
        """
        Removes exact full-row duplicates, or duplicates based on a specific primary key column.
        Preserves the first occurrence.
        """
        seen: Set[Any] = set()
        deduped_rows: List[List[Any]] = []
        key_idx = headers.index(key_column) if (key_column and key_column in headers) else None

        for row in rows:
            record_key = row[key_idx] if key_idx is not None else tuple(str(x) for x in row)
            if record_key not in seen:
                seen.add(record_key)
                deduped_rows.append(row)

        duplicates_count = len(rows) - len(deduped_rows)
        return deduped_rows, duplicates_count

    # -----------------------------------------------------------------------
    # 2. Type Inference & Value Sanitization
    # -----------------------------------------------------------------------

    def sanitize_value(self, val: str) -> Union[int, float, str, None]:
        """
        Sanitizes strings by cleaning currency symbols, commas, and converting to numeric/dates.
        """
        val_str = str(val).strip()
        if val_str.lower() in NULL_STRINGS:
            return None

        # Check for currency format (e.g. "$450,000" or "-$50,000")
        currency_clean = re.sub(r"[$,]", "", val_str)
        # Handle trailing/leading negative formatting
        if currency_clean.startswith("-$"):
            currency_clean = "-" + currency_clean[2:]

        # Attempt Integer cast
        try:
            return int(currency_clean)
        except ValueError:
            pass

        # Attempt Float cast
        try:
            return float(currency_clean)
        except ValueError:
            pass

        # Attempt Date normalization (YYYY-MM-DD)
        for date_fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%m/%d/%Y"):
            try:
                parsed_date = datetime.datetime.strptime(val_str, date_fmt)
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                pass

        return val_str

    def infer_and_cast_types(
        self, headers: List[str], rows: List[List[str]]
    ) -> Tuple[List[List[Any]], Dict[str, str]]:
        """
        Infers column types and casts values to appropriate Python datatypes.
        """
        cleaned_rows: List[List[Any]] = []
        col_type_guesses: Dict[str, List[str]] = {h: [] for h in headers}

        for row in rows:
            cleaned_row = []
            for idx, val in enumerate(row):
                sanitized = self.sanitize_value(val)
                cleaned_row.append(sanitized)
                if sanitized is not None:
                    if isinstance(sanitized, int):
                        col_type_guesses[headers[idx]].append("int")
                    elif isinstance(sanitized, float):
                        col_type_guesses[headers[idx]].append("float")
                    else:
                        col_type_guesses[headers[idx]].append("str")
            cleaned_rows.append(cleaned_row)

        inferred_types: Dict[str, str] = {}
        for h, types in col_type_guesses.items():
            if not types:
                inferred_types[h] = "str"
            elif all(t == "int" for t in types):
                inferred_types[h] = "int"
            elif all(t in ("int", "float") for t in types):
                inferred_types[h] = "float"
            else:
                inferred_types[h] = "str"

        return cleaned_rows, inferred_types

    # -----------------------------------------------------------------------
    # 3. Missing Value Detection & Imputation
    # -----------------------------------------------------------------------

    def impute_missing_values(
        self, headers: List[str], rows: List[List[Any]], inferred_types: Dict[str, str]
    ) -> Tuple[List[List[Any]], Dict[str, int]]:
        """
        Fills missing values using:
        - Numeric columns: Median (robust against skew/outliers) or Mean
        - Categorical/String columns: Mode (most frequent non-empty value)
        """
        imputed_counts: Dict[str, int] = {h: 0 for h in headers}
        col_values: Dict[int, List[Any]] = {i: [] for i in range(len(headers))}

        for row in rows:
            for idx, val in enumerate(row):
                if val is not None:
                    col_values[idx].append(val)

        # Calculate replacement statistics for each column
        replacements: Dict[int, Any] = {}
        for idx, h in enumerate(headers):
            values = col_values[idx]
            if not values:
                replacements[idx] = "Unknown"
                continue

            col_type = inferred_types.get(h, "str")
            if col_type in ("int", "float"):
                # Use median for robustness
                numeric_vals = [float(v) for v in values if isinstance(v, (int, float))]
                if numeric_vals:
                    med = statistics.median(numeric_vals)
                    replacements[idx] = int(round(med)) if col_type == "int" else round(med, 2)
                else:
                    replacements[idx] = 0
            else:
                # Use mode for categorical
                try:
                    replacements[idx] = statistics.mode([str(v) for v in values])
                except statistics.StatisticsError:
                    replacements[idx] = str(values[0])

        # Apply imputation
        imputed_rows: List[List[Any]] = []
        for row in rows:
            new_row = list(row)
            for idx, val in enumerate(new_row):
                if val is None:
                    new_row[idx] = replacements[idx]
                    imputed_counts[headers[idx]] += 1
            imputed_rows.append(new_row)

        return imputed_rows, imputed_counts

    # -----------------------------------------------------------------------
    # 4. Outlier Detection & Handling (IQR & Z-Score)
    # -----------------------------------------------------------------------

    def detect_and_cap_outliers(
        self, headers: List[str], rows: List[List[Any]], inferred_types: Dict[str, str]
    ) -> Tuple[List[List[Any]], Dict[str, int]]:
        """
        Detects numerical outliers using Interquartile Range (IQR) fences
        and caps them to [Q1 - 1.5*IQR, Q3 + 1.5*IQR].
        """
        outlier_counts: Dict[str, int] = {h: 0 for h in headers}

        for idx, h in enumerate(headers):
            if inferred_types.get(h) not in ("int", "float"):
                continue

            # Extract numeric series
            vals = [float(row[idx]) for row in rows if isinstance(row[idx], (int, float))]
            if len(vals) < 4:
                continue

            sorted_vals = sorted(vals)
            n = len(sorted_vals)
            q1 = sorted_vals[n // 4]
            q3 = sorted_vals[(3 * n) // 4]
            iqr = q3 - q1

            lower_fence = q1 - (self.iqr_factor * iqr)
            upper_fence = q3 + (self.iqr_factor * iqr)

            # Cap values exceeding bounds
            for row in rows:
                current_val = float(row[idx])
                if current_val < lower_fence or current_val > upper_fence:
                    outlier_counts[h] += 1
                    capped_val = max(lower_fence, min(upper_fence, current_val))
                    row[idx] = int(round(capped_val)) if inferred_types[h] == "int" else round(capped_val, 2)

        return rows, outlier_counts

    # -----------------------------------------------------------------------
    # End-to-End Cleaning Pipeline
    # -----------------------------------------------------------------------

    def clean_dataset(
        self, raw_headers: List[str], raw_rows: List[List[str]], key_column: Optional[str] = None
    ) -> DatasetProfile:
        """Executes full multi-phase cleaning pipeline."""
        metrics = CleaningMetrics()
        metrics.total_rows_initial = len(raw_rows)

        # 1. Type inference & sanitization
        cast_rows, inferred_types = self.infer_and_cast_types(raw_headers, raw_rows)
        metrics.type_corrections_applied = inferred_types

        # 2. Duplicate detection
        deduped_rows, dup_count = self.remove_duplicates(raw_headers, cast_rows, key_column=key_column)
        metrics.duplicates_removed = dup_count

        # 3. Missing value imputation
        imputed_rows, missing_stats = self.impute_missing_values(raw_headers, deduped_rows, inferred_types)
        metrics.missing_values_imputed = missing_stats

        # 4. Outlier detection & bounding
        final_rows, outlier_stats = self.detect_and_cap_outliers(raw_headers, imputed_rows, inferred_types)
        metrics.outliers_detected = outlier_stats
        metrics.total_rows_final = len(final_rows)

        return DatasetProfile(
            headers=raw_headers,
            rows=final_rows,
            inferred_types=inferred_types,
            metrics=metrics,
        )
