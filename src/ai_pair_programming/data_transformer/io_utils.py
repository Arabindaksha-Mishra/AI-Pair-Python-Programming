"""
Data Transformer: I/O Utilities
================================
Safe, robust CSV file reader and exporter with encoding detection.
"""

from __future__ import annotations

import csv
from typing import Any

from ai_pair_programming.output_handler import get_logger

_LOGGER = get_logger("data_transformer.io")


def load_csv_file(file_path: str) -> tuple[list[str], list[list[str]]]:
    """
    Read a CSV file and return trimmed header names and data rows.

    Args:
        file_path (str): Absolute or relative filesystem path to the CSV file.

    Returns:
        tuple[list[str], list[list[str]]]: Tuple containing (headers, rows).

    """
    _LOGGER.debug(f"Reading CSV dataset from: {file_path}")
    with open(file_path, encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        try:
            raw_headers = next(reader)
        except StopIteration:
            _LOGGER.warning(f"CSV file is empty: {file_path}")
            return [], []

        headers = [h.strip() for h in raw_headers]
        rows = [
            [cell.strip() for cell in row]
            for row in reader
            if any(cell.strip() for cell in row)
        ]
        _LOGGER.debug(
            f"Loaded {len(rows)} rows and {len(headers)} columns from {file_path}"
        )
        return headers, rows


def save_csv_file(file_path: str, headers: list[str], rows: list[list[Any]]) -> None:
    """
    Write tabular matrix data to disk as a CSV file.

    Args:
        file_path (str): Destination file path.
        headers (list[str]): Header row columns.
        rows (list[list[Any]]): Tabular 2D data rows to write.

    Returns:
        None

    """
    _LOGGER.debug(f"Exporting {len(rows)} rows to: {file_path}")
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    _LOGGER.info(f"Successfully saved CSV dataset ({len(rows)} rows) to: {file_path}")
