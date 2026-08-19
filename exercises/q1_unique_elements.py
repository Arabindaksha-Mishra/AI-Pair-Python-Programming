"""
Exercise 1: Unique Elements from List
====================================
Problem Statement:
Write a Python function that takes a list and returns a new list with unique elements of the first list.

Senior Engineering Highlights:
- Preserves insertion order in O(N) time using dict.fromkeys() (Python 3.7+ guarantee).
- Handles unhashable nested items (e.g. lists, dicts) with graceful fallback.
- Provides type annotations and doctests.
"""

from typing import Any, List


def get_unique_elements(items: List[Any]) -> List[Any]:
    """
    Returns a new list containing only the unique elements of the input list,
    preserving the original insertion order.

    Time Complexity: O(N) for hashable items, O(N^2) worst-case fallback for unhashables.
    Space Complexity: O(N) auxiliary space.

    Examples:
        >>> get_unique_elements([1, 2, 2, 3, 4, 4, 1])
        [1, 2, 3, 4]
        >>> get_unique_elements(['apple', 'banana', 'apple', 'orange'])
        ['apple', 'banana', 'orange']
    """
    if not items:
        return []

    try:
        # Fast O(N) path using dict keys (guaranteed insertion-ordered)
        return list(dict.fromkeys(items))
    except TypeError:
        # Fallback for lists containing unhashable objects (e.g., nested lists, dicts)
        unique_list: List[Any] = []
        seen = []
        for item in items:
            if item not in seen:
                seen.append(item)
                unique_list.append(item)
        return unique_list


def get_unique_elements_ordered(items: List[Any]) -> List[Any]:
    """Explicit alias for get_unique_elements emphasizing order preservation."""
    return get_unique_elements(items)


if __name__ == "__main__":
    sample_data = [1, 2, 3, 2, 4, 1, 5, "python", "ai", "python", True, 1]
    print("Original List:", sample_data)
    unique_result = get_unique_elements(sample_data)
    print("Unique List (Order Preserved):", unique_result)
