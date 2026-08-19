"""
Domain Group 1: Collections & Set Algebra (Python 3.12+)
=========================================================
Covers:
1. Unique Elements with Insertion-Order Preservation (Q1)
2. Set Operations: Union & Symmetric Difference (Q10)

100% Python Standard Library (No external dependencies).
"""

from collections.abc import Iterable
from typing import Any

from ai_pair_programming.data_transformer.deduplicator import deduplicate_list
from ai_pair_programming.telemetry import get_logger

_LOGGER = get_logger("algorithms.collections")


def get_unique_elements(items: list[Any]) -> list[Any]:
    """
    Return unique elements from input list while preserving insertion order.

    Args:
        items (list[Any]): Input collection containing items to deduplicate.

    Returns:
        list[Any]: New list containing unique items in original insertion order.

    """
    return deduplicate_list(items)


def merge_sets_unique(set_a: Iterable[Any], set_b: Iterable[Any]) -> set[Any]:
    """
    Compute set union combining all unique items across two collections.

    Args:
        set_a (Iterable[Any]): First collection of elements.
        set_b (Iterable[Any]): Second collection of elements.

    Returns:
        set[Any]: Unified set containing all unique elements from both inputs.

    """
    s_a = set(set_a)
    s_b = set(set_b)
    return s_a | s_b


def symmetric_difference_unique(set_a: Iterable[Any], set_b: Iterable[Any]) -> set[Any]:
    """
    Compute symmetric difference of elements present in exactly one collection.

    Args:
        set_a (Iterable[Any]): First collection of elements.
        set_b (Iterable[Any]): Second collection of elements.

    Returns:
        set[Any]: Set of elements present in either set_a or set_b, but not both.

    """
    s_a = set(set_a)
    s_b = set(set_b)
    return s_a ^ s_b


def demonstrate_all_set_operations(
    set_a: set[Any], set_b: set[Any]
) -> tuple[set[Any], set[Any], set[Any]]:
    """
    Compute union, intersection, and symmetric difference for two sets.

    Args:
        set_a (set[Any]): First input set.
        set_b (set[Any]): Second input set.

    Returns:
        tuple[set[Any], set[Any], set[Any]]: Results of union, intersection,
            and symmetric difference operations.

    """
    union_res = set_a | set_b
    intersect_res = set_a & set_b
    sym_diff_res = set_a ^ set_b
    return union_res, intersect_res, sym_diff_res


if __name__ == "__main__":
    print("--- 1. Unique Elements Demo ---")
    raw_list = [10, 20, 20, 30, 40, 10, 50, 30]
    print(f"Original: {raw_list}")
    print(f"Unique:   {get_unique_elements(raw_list)}")

    print("\n--- 2. Set Operations Demo ---")
    set1 = {10, 20, 30, 40, 50}
    set2 = {30, 40, 50, 60, 70}
    print(f"Set A: {set1}")
    print(f"Set B: {set2}")
    print(f"Union (A ∪ B):           {merge_sets_unique(set1, set2)}")
    print(f"Symmetric Diff (A Δ B):  {symmetric_difference_unique(set1, set2)}")
