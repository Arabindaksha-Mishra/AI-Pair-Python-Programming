"""
Module 3: Digit Permutations & Integer Mathematics (Python 3.12+)
==================================================================
Comprehensive implementation for computing the mathematical difference
between the largest and smallest numbers formed by the digits of a number (Q3).
"""

from __future__ import annotations


def digit_difference(n: int | str) -> int:
    """
    Calculate difference between max and min digit permutations.

    Sorts the constituent digits in descending order to form the largest
    possible number, and in ascending order to form the smallest possible
    number, then returns their mathematical difference.

    Args:
        n (int | str): Input integer or string of digits.

    Returns:
        int: Difference (Largest Formed Number - Smallest Formed Number).

    Raises:
        ValueError: If input is negative or contains non-digit characters.

    """
    raw_str = str(n).strip()
    if not raw_str.isdigit():
        raise ValueError(
            f"Input must contain non-negative digits only, received: {n!r}"
        )

    digits = list(raw_str)
    max_num = int("".join(sorted(digits, reverse=True)))
    min_num = int("".join(sorted(digits)))

    return max_num - min_num


def get_digit_extremes(n: int | str) -> tuple[int, int, int]:
    """
    Return (max_permutation, min_permutation, difference) tuple for a number.

    Args:
        n (int | str): Input integer or digit string.

    Returns:
        tuple[int, int, int]: (Largest Formed, Smallest Formed, Difference).

    """
    raw_str = str(n).strip()
    if not raw_str.isdigit():
        raise ValueError(f"Input must contain digits only, received: {n!r}")

    digits = list(raw_str)
    max_val = int("".join(sorted(digits, reverse=True)))
    min_val = int("".join(sorted(digits)))
    return max_val, min_val, max_val - min_val


def main() -> None:
    """
    Demonstrate Module 3 digit difference algorithms.

    Returns:
        None

    """
    print("==================================================================")
    print("   🔢 MODULE 3: DIGIT DIFFERENCE & PERMUTATION ANALYSIS           ")
    print("==================================================================")
    samples = ["213", "1234", 9051, "8008", 7, 987654321]
    for s in samples:
        max_v, min_v, diff = get_digit_extremes(s)
        print(f"Input: {s!s:>9} -> Max({max_v:>9}) - Min({min_v:>9}) = {diff:>9}")
    print("==================================================================\n")


if __name__ == "__main__":
    main()
