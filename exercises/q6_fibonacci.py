"""
Exercise 6: Fibonacci Series (Recursive vs. Non-Recursive)
=========================================================
Problem Statement:
Display the Fibonacci series with recursion and without recursion.

Definitions:
F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2) for n >= 2.
Sequence for n=10: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

Senior Engineering Highlights:
- Recursive Approach: Pure recursion vs. Memoized recursion (functools.lru_cache) to eliminate exponential O(2^N) call trees.
- Non-Recursive Approach (Iterative): O(N) time with O(1) auxiliary space using two pointers.
- Streaming Approach (Generator): Lazy O(1) memory evaluation via yield.
"""

from functools import lru_cache
from typing import Generator, List


# ---------------------------------------------------------------------------
# 1. Recursive Implementations
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1024)
def _fib_recursive_term(n: int) -> int:
    """Computes n-th Fibonacci number using memoized recursion."""
    if n < 0:
        raise ValueError("Fibonacci index must be non-negative.")
    if n > 500:
        raise ValueError("Fibonacci recursive depth limit exceeded (max: 500). Use fibonacci_iterative instead.")
    if n in (0, 1):
        return n
    return _fib_recursive_term(n - 1) + _fib_recursive_term(n - 2)


def fibonacci_recursive(count: int) -> List[int]:
    """
    Generates a list of the first `count` Fibonacci numbers using recursion.

    Time Complexity: O(count) with LRU caching (O(2^count) without memoization).
    Space Complexity: O(count) recursion stack & cache.
    """
    if count <= 0:
        return []
    return [_fib_recursive_term(i) for i in range(count)]


# ---------------------------------------------------------------------------
# 2. Non-Recursive (Iterative) Implementation
# ---------------------------------------------------------------------------

def fibonacci_iterative(count: int) -> List[int]:
    """
    Generates a list of the first `count` Fibonacci numbers iteratively.

    Time Complexity: O(count)
    Space Complexity: O(1) auxiliary space (excluding returned list).
    """
    if count <= 0:
        return []
    if count == 1:
        return [0]

    series: List[int] = [0, 1]
    a, b = 0, 1
    for _ in range(2, count):
        a, b = b, a + b
        series.append(b)
    return series


# ---------------------------------------------------------------------------
# 3. Generator (Streaming / Lazy Evaluation)
# ---------------------------------------------------------------------------

def fibonacci_generator(count: int) -> Generator[int, None, None]:
    """
    Yields Fibonacci numbers one-by-one lazily.

    Time Complexity: O(count)
    Space Complexity: O(1) total memory footprint.
    """
    if count <= 0:
        return
    a, b = 0, 1
    for i in range(count):
        if i == 0:
            yield a
        elif i == 1:
            yield b
        else:
            a, b = b, a + b
            yield b


if __name__ == "__main__":
    n_terms = 10
    print(f"--- Fibonacci Comparison (First {n_terms} Terms) ---")
    rec_result = fibonacci_recursive(n_terms)
    iter_result = fibonacci_iterative(n_terms)
    gen_result = list(fibonacci_generator(n_terms))

    print(f"1. Recursive Series:     {rec_result}")
    print(f"2. Iterative Series:     {iter_result}")
    print(f"3. Generator Series:     {gen_result}")
    print(f"All outputs identical?   {rec_result == iter_result == gen_result}")
