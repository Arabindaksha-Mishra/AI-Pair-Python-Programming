"""
Exercise 10: Set Operations & Duplicate Elimination
===================================================
Problem Statement:
Python program to return a new set with unique items from both sets by removing duplicates.

Mathematical & Set Theory Clarification:
In Python set algebra, combining two sets while eliminating duplicates corresponds to:
1. Set Union (A ∪ B): Combines all elements from set A and set B, automatically
   enforcing uniqueness (eliminating duplicate occurrences across sets).
2. Symmetric Difference (A Δ B): Selects elements that are in either A or B,
   but NOT in their intersection (A ∩ B).

Senior Engineering Highlights:
- Implements both interpretations with clear set operator syntax (`|` and `^`).
- Zero mutation of original input sets (pure functions).
- Accepts arbitrary iterables and converts them safely to sets.
"""

from typing import Any, Iterable, Set, Tuple


def merge_sets_unique(set_a: Iterable[Any], set_b: Iterable[Any]) -> Set[Any]:
    """
    Returns a new set containing all unique items across both sets (Set Union: A ∪ B).
    Any item appearing in both sets is represented only once.

    Time Complexity: O(len(set_a) + len(set_b))
    Space Complexity: O(len(set_a) + len(set_b))

    Examples:
        >>> merge_sets_unique({1, 2, 3}, {3, 4, 5})
        {1, 2, 3, 4, 5}
        >>> merge_sets_unique(['python', 'c++'], ['java', 'python'])
        {'c++', 'java', 'python'}
    """
    s_a = set(set_a)
    s_b = set(set_b)
    # Using union operator (|) or method .union()
    return s_a | s_b


def symmetric_difference_unique(set_a: Iterable[Any], set_b: Iterable[Any]) -> Set[Any]:
    """
    Returns items that are unique to each set (i.e. excluding elements present in both).
    Symmetric Difference: (A ∪ B) - (A ∩ B).

    Examples:
        >>> symmetric_difference_unique({1, 2, 3}, {3, 4, 5})
        {1, 2, 4, 5}
    """
    s_a = set(set_a)
    s_b = set(set_b)
    return s_a ^ s_b


def demonstrate_all_set_operations(set_a: Set[Any], set_b: Set[Any]) -> Tuple[Set[Any], Set[Any], Set[Any]]:
    """Helper to return (Union, Intersection, Symmetric Difference)."""
    union_res = set_a | set_b
    intersect_res = set_a & set_b
    sym_diff_res = set_a ^ set_b
    return union_res, intersect_res, sym_diff_res


if __name__ == "__main__":
    set1 = {10, 20, 30, 40, 50}
    set2 = {30, 40, 50, 60, 70}

    print(f"Set 1: {set1}")
    print(f"Set 2: {set2}")

    merged = merge_sets_unique(set1, set2)
    print(f"\n1. New Set with Unique Items from Both (Union A ∪ B):")
    print(f"   Result: {merged}")

    sym_diff = symmetric_difference_unique(set1, set2)
    print(f"\n2. Items Exclusive to Either Set (Symmetric Diff A Δ B):")
    print(f"   Result: {sym_diff}")
