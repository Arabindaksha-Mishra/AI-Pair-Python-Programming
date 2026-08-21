"""
Module 1: Unique Elements & Set Algebra (Python 3.12+)
======================================================
Comprehensive implementations for:
1. Order-Preserved List Deduplication (Q1)
2. Set Union & Symmetric Difference Deduplication (Q10)

Adheres strictly to Clean Code principles and standard library purity.
"""

from __future__ import annotations

from typing import Any


def unique_elements(items: list[Any]) -> list[Any]:
    """
    Return a new list containing unique elements while preserving order.

    Uses dictionary key hashing (dict.fromkeys) to achieve O(N) linear time
    complexity while guaranteeing that the chronological sequence of the
    first occurrence of each element is preserved.

    Args:
        items (list[T]): Input sequence of potentially duplicate elements.

    Returns:
        list[T]: New list containing only distinct elements in first-seen order.

    """
    return list(dict.fromkeys(items))


def set_union_and_difference(
    set1: set[Any], set2: set[Any]
) -> tuple[set[Any], set[Any]]:
    """
    Compute total union and symmetric difference between two input sets.

    Args:
        set1 (set[Any]): First collection of distinct elements.
        set2 (set[Any]): Second collection of distinct elements.

    Returns:
        tuple[set[Any], set[Any]]: Tuple containing:
            1. Total Union (A | B) - All distinct items across both sets.
            2. Symmetric Difference (A ^ B) - Items in either set, but not both.

    """
    union_res: set[Any] = set1 | set2
    sym_diff_res: set[Any] = set1 ^ set2
    return union_res, sym_diff_res


def main() -> None:
    """
    Demonstrate Module 1 unique elements and set operations.

    Returns:
        None

    """
    print("==================================================================")
    print("   📦 MODULE 1: UNIQUE ELEMENTS & SET DEDUPLICATION ALGEBRA      ")
    print("==================================================================")
    sample_list: list[Any] = [1, 2, 2, 3, 4, 4, 1, "apple", "banana", "apple"]
    print(f"Original Input List : {sample_list}")
    print(f"Deduplicated List   : {unique_elements(sample_list)}")

    s1 = {"Python", "TypeScript", "Rust", "Go"}
    s2 = {"Go", "Java", "Python", "C++"}
    union_s, diff_s = set_union_and_difference(s1, s2)
    print(f"\nSet 1                : {sorted(s1)}")
    print(f"Set 2                : {sorted(s2)}")
    print(f"Union (All Unique)   : {sorted(union_s)}")
    print(f"Symmetric Difference : {sorted(diff_s)}")
    print("==================================================================\n")


if __name__ == "__main__":
    main()
