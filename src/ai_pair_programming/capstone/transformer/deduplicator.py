"""
Data Transformer: Deduplication Engine
=======================================
Provides modular algorithms for removing duplicate records while preserving
insertion order, and deduplicating tabular matrices based on primary keys.
"""

from __future__ import annotations

from typing import Any

from ai_pair_programming.telemetry import get_logger

_LOGGER = get_logger("data_transformer.deduplicator")


def _deduplicate_unhashables(items: list[Any]) -> list[Any]:
    """
    Deduplicate unhashable objects while preserving insertion order.

    Args:
        items (list[Any]): Collection containing unhashable elements.

    Returns:
        list[Any]: Deduplicated collection in original order.

    """
    seen: list[Any] = []
    unique: list[Any] = []
    for item in items:
        if item not in seen:
            seen.append(item)
            unique.append(item)
    return unique


def deduplicate_list(items: list[Any]) -> list[Any]:
    """
    Deduplicate a list while preserving original insertion order.

    Args:
        items (list[Any]): Collection of items to deduplicate.

    Returns:
        list[Any]: Deduplicated list in original insertion order.

    """
    if not items:
        return []
    try:
        return list(dict.fromkeys(items))
    except TypeError:
        return _deduplicate_unhashables(items)


def _extract_row_key(row: list[Any], key_idx: int | None) -> Any:
    """
    Extract primary key cell or entire row tuple for uniqueness comparison.

    Args:
        row (list[Any]): Tabular row cells.
        key_idx (int | None): Column index of primary key if present.

    Returns:
        Any: Distinct row identity key.

    """
    if key_idx is not None and key_idx < len(row):
        return row[key_idx]
    return tuple(row)


def deduplicate_tabular_rows(
    headers: list[str],
    rows: list[list[Any]],
    key_column: str | None = None,
) -> tuple[list[list[Any]], int]:
    """
    Remove exact duplicate rows or key-based duplicate records from matrix.

    Args:
        headers (list[str]): Column header names.
        rows (list[list[Any]]): Tabular 2D data rows.
        key_column (str | None): Optional primary key header to deduplicate on.

    Returns:
        tuple[list[list[Any]], int]: (deduplicated_rows, count_removed).

    """
    if not rows:
        return [], 0

    key_idx = (
        headers.index(key_column) if key_column and key_column in headers else None
    )
    seen_keys: set[Any] = set()
    deduped_rows: list[list[Any]] = []
    duplicates_count = 0

    for row in rows:
        row_key = _extract_row_key(row, key_idx)
        if row_key in seen_keys:
            duplicates_count += 1
            continue
        seen_keys.add(row_key)
        deduped_rows.append(row)

    return deduped_rows, duplicates_count
