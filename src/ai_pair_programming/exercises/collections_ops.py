"""
Domain Group 1: Collections & Set Algebra (Python 3.12+)
=========================================================
Covers:
1. Unique Elements with Insertion-Order Preservation (Q1)
2. Set Operations: Union & Symmetric Difference (Q10)

100% Python Standard Library.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def get_unique_elements(items: list[Any]) -> list[Any]:
    """Return unique elements preserving original insertion order."""
    seen: set[Any] = set()
    unique: list[Any] = []
    for item in items:
        try:
            if item not in seen:
                seen.add(item)
                unique.append(item)
        except TypeError:
            if item not in unique:
                unique.append(item)
    return unique


def merge_sets_unique(set_a: Iterable[Any], set_b: Iterable[Any]) -> set[Any]:
    """Compute set union combining all unique items across two collections."""
    return set(set_a) | set(set_b)


def symmetric_difference_unique(set_a: Iterable[Any], set_b: Iterable[Any]) -> set[Any]:
    """Compute symmetric difference of elements present in exactly one collection."""
    return set(set_a) ^ set(set_b)
