"""
Module 4: Sequence Engineering & Fibonacci Series (Python 3.12+)
================================================================
Comprehensive dual-mode implementations of Fibonacci sequence:
1. Memoized Dynamic Programming Recursion (Q6)
2. Constant Auxiliary Space Iteration (Q6)
"""

from __future__ import annotations

from collections.abc import Generator
from functools import lru_cache


@lru_cache(maxsize=1024)
def fibonacci_recursive(n: int) -> int:
    """
    Compute the n-th Fibonacci number using memoized recursion.

    Base Cases: F(0) = 0, F(1) = 1.
    Recursive Step: F(n) = F(n-1) + F(n-2).

    Args:
        n (int): Non-negative index in Fibonacci sequence.

    Returns:
        int: Value of n-th Fibonacci term.

    Raises:
        ValueError: If n is negative.

    """
    if not isinstance(n, int) or n < 0:
        raise ValueError(f"Fibonacci index must be non-negative, got {n!r}")
    if n in (0, 1):
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n: int) -> list[int]:
    """
    Generate the first n terms of the Fibonacci sequence iteratively.

    Uses O(1) auxiliary space variables to achieve O(N) runtime.

    Args:
        n (int): Number of Fibonacci terms to produce (count).

    Returns:
        list[int]: Sequence of first n Fibonacci terms starting from 0.

    Raises:
        ValueError: If n is negative.

    """
    if not isinstance(n, int) or n < 0:
        raise ValueError(f"Count of terms must be non-negative, got {n!r}")
    if n == 0:
        return []
    if n == 1:
        return [0]

    series: list[int] = [0, 1]
    a, b = 0, 1
    for _ in range(2, n):
        a, b = b, a + b
        series.append(b)

    return series


def fibonacci_generator(limit: int) -> Generator[int, None, None]:
    """
    Yield Fibonacci terms lazily using a Python generator.

    Args:
        limit (int): Maximum number of terms to yield.

    Yields:
        int: Successive Fibonacci terms.

    """
    a, b = 0, 1
    for _ in range(limit):
        yield a
        a, b = b, a + b


def main() -> None:
    """
    Demonstrate Module 4 Fibonacci algorithms.

    Returns:
        None

    """
    print("==================================================================")
    print("   🔢 MODULE 4: FIBONACCI (RECURSION, ITERATION, GENERATOR)       ")
    print("==================================================================")
    count = 12
    print(f"First {count} terms (Iterative) : {fibonacci_iterative(count)}")
    print(f"First {count} terms (Generator) : {list(fibonacci_generator(count))}")
    print("\nRecursive Verification for Selected Terms:")
    for idx in [0, 1, 5, 10, 15, 20]:
        print(f"  F({idx:>2}) = {fibonacci_recursive(idx)}")
    print("==================================================================\n")


if __name__ == "__main__":
    main()
