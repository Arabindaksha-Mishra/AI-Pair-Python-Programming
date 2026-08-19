"""
Exercise 2: Perfect Number Validator
====================================
Problem Statement:
Write a Python function to check whether a number is perfect or not.

Definition:
A positive integer is perfect if it equals the sum of its proper positive divisors
(i.e., all positive divisors excluding the number itself).

Examples:
- 6  -> 1 + 2 + 3 = 6 (True)
- 28 -> 1 + 2 + 4 + 7 + 14 = 28 (True)
- 496 -> True
- 8128 -> True

Senior Engineering Highlights:
- O(sqrt(N)) time complexity by checking divisor pairs up to sqrt(N).
- Handles edge cases: n <= 1 is False (including negatives, 0, and 1).
- Includes helper to find perfect numbers within a range.
"""

import math
from typing import List


def is_perfect_number(n: int) -> bool:
    """
    Checks whether a given integer is a perfect number.

    Time Complexity: O(sqrt(n))
    Space Complexity: O(1)

    Args:
        n: The integer to test.

    Returns:
        True if n is a perfect number, False otherwise.

    Examples:
        >>> is_perfect_number(6)
        True
        >>> is_perfect_number(28)
        True
        >>> is_perfect_number(12)
        False
        >>> is_perfect_number(1)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int) or n <= 1:
        return False

    # 1 is always a proper divisor for n > 1
    divisor_sum = 1
    sqrt_n = int(math.isqrt(n))

    # Test divisors from 2 up to sqrt(n)
    for i in range(2, sqrt_n + 1):
        if n % i == 0:
            divisor_sum += i
            paired_divisor = n // i
            if paired_divisor != i:  # Avoid adding square root twice
                divisor_sum += paired_divisor

    return divisor_sum == n


def find_perfect_numbers_in_range(start: int, end: int) -> List[int]:
    """Finds all perfect numbers in the inclusive range [start, end]."""
    return [num for num in range(max(2, start), end + 1) if is_perfect_number(num)]


if __name__ == "__main__":
    test_cases = [6, 28, 496, 8128, 12, 1, 0, -6]
    print("--- Perfect Number Validation ---")
    for num in test_cases:
        result = is_perfect_number(num)
        print(f"Number: {num:5d} -> Is Perfect: {result}")

    print("\nPerfect numbers between 1 and 10,000:", find_perfect_numbers_in_range(1, 10000))
