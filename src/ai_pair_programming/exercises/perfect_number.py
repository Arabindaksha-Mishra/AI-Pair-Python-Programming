"""
Module 2: Number Theory & Perfect Numbers (Python 3.12+)
========================================================
Comprehensive implementation of square-root bound divisor summation
to verify perfect numbers and search ranges for perfect integers (Q2).
"""

from __future__ import annotations

import math


def is_perfect_number(n: int) -> bool:
    """
    Check if a given integer is a perfect number in O(sqrt(N)) time.

    A perfect number equals the sum of its proper positive divisors.
    Divisors are paired (d and n // d) up to the integer square root of n.

    Args:
        n (int): Integer candidate to evaluate.

    Returns:
        bool: True if n is a perfect number, False otherwise.

    """
    if not isinstance(n, int) or n <= 1:
        return False

    divisor_sum: int = 1
    sqrt_limit: int = math.isqrt(n)

    for divisor in range(2, sqrt_limit + 1):
        if n % divisor == 0:
            divisor_sum += divisor
            paired_divisor = n // divisor
            if paired_divisor != divisor:
                divisor_sum += paired_divisor

    return divisor_sum == n


def find_perfect_numbers_in_range(start: int, stop: int) -> list[int]:
    """
    Find all perfect numbers within a closed integer interval [start, stop].

    Args:
        start (int): Inclusive start integer.
        stop (int): Inclusive stop integer.

    Returns:
        list[int]: Sorted list of perfect numbers in interval.

    """
    return [num for num in range(max(1, start), stop + 1) if is_perfect_number(num)]


def main() -> None:
    """
    Demonstrate Module 2 perfect number algorithms.

    Returns:
        None

    """
    print("==================================================================")
    print("   🔢 MODULE 2: PERFECT NUMBER CHECKER & RANGE SEARCH             ")
    print("==================================================================")
    test_candidates = [6, 28, 496, 8128, 12, 100, 33550336]
    for num in test_candidates:
        result = is_perfect_number(num)
        status = "✅ PERFECT" if result else "❌ NOT PERFECT"
        print(f"Number {num:>10} -> {status}")

    print("\nSearching for all perfect numbers between 1 and 10,000:")
    found = find_perfect_numbers_in_range(1, 10000)
    print(f"Result: {found}")
    print("==================================================================\n")


if __name__ == "__main__":
    main()
