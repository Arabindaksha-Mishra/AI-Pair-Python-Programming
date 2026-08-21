"""
Domain Group 2: Numerical Mathematics (Python 3.12+)
======================================================
Covers:
1. Square-root limit Perfect Number search (Q2)
2. Digit Permutation Difference analysis (Q3)
3. Memoized Recursive & Iterative Fibonacci Generator (Q6)
4. Continue Statement Modulo Skipping (Q8)
"""

from __future__ import annotations

from collections.abc import Generator
from functools import lru_cache
import math


def is_perfect_number(n: int) -> bool:
    """Determine if integer n is a perfect number."""
    if n <= 1:
        return False
    divisor_sum = 1
    sqrt_n = math.isqrt(n)
    for i in range(2, sqrt_n + 1):
        if n % i == 0:
            divisor_sum += i
            pair = n // i
            if pair != i:
                divisor_sum += pair
    return divisor_sum == n


def find_perfect_numbers_in_range(start: int, end: int) -> list[int]:
    """Find all perfect numbers in range [start, end]."""
    return [n for n in range(max(1, start), end + 1) if is_perfect_number(n)]


def digit_difference(n: int | str) -> int:
    """
    Calculate difference between max and min digit permutations.

    Args:
        n (int | str): Input integer or string of digits.

    Returns:
        int: Difference (Max Permutation - Min Permutation).
    """
    raw_str = str(n).strip()
    if not raw_str.isdigit():
        err_msg = f"Input must contain digits only, received: {n!r}"
        raise ValueError(err_msg)

    digits = list(raw_str)
    max_num = int("".join(sorted(digits, reverse=True)))
    min_num = int("".join(sorted(digits)))
    return max_num - min_num


def fibonacci_iterative(n: int) -> list[int]:
    """Generate first n Fibonacci terms iteratively."""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq


@lru_cache(maxsize=128)
def _fib_memo(k: int) -> int:
    """
    Compute single Fibonacci number recursively with memoization.

    Args:
        k (int): Term index.

    Returns:
        int: Fibonacci value at index k.

    """
    if k <= 0:
        return 0
    if k == 1:
        return 1
    return _fib_memo(k - 1) + _fib_memo(k - 2)


def fibonacci_recursive(n: int) -> list[int]:
    """Generate first n Fibonacci terms recursively with memoization."""
    if n <= 0:
        return []
    return [_fib_memo(i) for i in range(n)]


def fibonacci_generator(n: int) -> Generator[int, None, None]:
    """Yield Fibonacci terms lazily."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def square_odd_numbers_loop(limit: int = 10) -> list[tuple[int, int]]:
    """Compute (odd_number, odd_number**2) tuples skipping evens via continue."""
    results: list[tuple[int, int]] = []
    for i in range(1, limit):
        if i % 2 == 0:
            continue
        results.append((i, i**2))
    return results
