"""
Domain Group 2: Numerical Mathematics & Sequences
==================================================
Covers:
1. Perfect Number Validator with O(sqrt(N)) Divisor Search (Q2)
2. Digit Permutation Extrema Difference (Q3)
3. Fibonacci Series (Recursive with LRU Cache, Iterative O(1) Space, Generator) (Q6)
4. Square Numbers with Parity Filter and 'continue' (Q8)

100% Python Standard Library (math, functools).
"""

from collections.abc import Generator
from functools import lru_cache
import math

from ai_pair_programming.telemetry import get_logger

_LOGGER = get_logger("algorithms.math")


def is_perfect_number(n: int) -> bool:
    """
    Check if an integer equals the sum of its proper positive divisors.

    Args:
        n (int): Target integer to evaluate.

    Returns:
        bool: True if n is a perfect number, False otherwise.

    """
    if isinstance(n, bool) or not isinstance(n, int) or n <= 1:
        return False

    divisor_sum = 1
    sqrt_n = math.isqrt(n)

    for i in range(2, sqrt_n + 1):
        if n % i == 0:
            divisor_sum += i
            paired = n // i
            if paired != i:
                divisor_sum += paired

    return divisor_sum == n


def find_perfect_numbers_in_range(start: int, end: int) -> list[int]:
    """
    Find all perfect numbers within an inclusive range [start, end].

    Args:
        start (int): Lower bound of the range.
        end (int): Upper bound of the range.

    Returns:
        list[int]: Sorted list of perfect numbers in the given range.

    """
    return [num for num in range(max(2, start), end + 1) if is_perfect_number(num)]


def digit_difference(number: int | str) -> int:
    """
    Calculate the difference between largest and smallest digit permutations.

    Args:
        number (int | str): Input numeric value or digit string.

    Returns:
        int: Value of max permutation minus min permutation.

    Raises:
        ValueError: If input contains no valid digits.

    """
    s = str(number).strip()
    digits = [c for c in s if c.isdigit()]
    if not digits:
        raise ValueError(f"Input '{number}' contains no valid numeric digits.")

    largest_str = "".join(sorted(digits, reverse=True))
    smallest_str = "".join(sorted(digits))

    return int(largest_str) - int(smallest_str)


@lru_cache(maxsize=1024)
def _fib_memoized(n: int) -> int:
    """
    Compute the n-th Fibonacci number using memoized recursion.

    Args:
        n (int): Non-negative Fibonacci index.

    Returns:
        int: Value of the n-th Fibonacci term.

    Raises:
        ValueError: If n is negative or exceeds recursion threshold (500).

    """
    if n < 0:
        raise ValueError("Fibonacci index must be non-negative.")
    if n > 500:
        raise ValueError(
            "Fibonacci recursive limit exceeded (max: 500). "
            "Use fibonacci_iterative instead."
        )
    if n in (0, 1):
        return n
    return _fib_memoized(n - 1) + _fib_memoized(n - 2)


def fibonacci_recursive(count: int) -> list[int]:
    """
    Generate the first `count` Fibonacci numbers using memoized recursion.

    Args:
        count (int): Total number of terms to generate.

    Returns:
        list[int]: Sequence of Fibonacci numbers up to count.

    """
    if count <= 0:
        return []
    return [_fib_memoized(i) for i in range(count)]


def fibonacci_iterative(count: int) -> list[int]:
    """
    Generate the first `count` Fibonacci numbers using O(1) space two-pointers.

    Args:
        count (int): Total number of terms to generate.

    Returns:
        list[int]: Sequence of Fibonacci numbers up to count.

    """
    if count <= 0:
        return []
    if count == 1:
        return [0]

    series: list[int] = [0, 1]
    a, b = 0, 1
    for _ in range(2, count):
        a, b = b, a + b
        series.append(b)
    return series


def fibonacci_generator(count: int) -> Generator[int, None, None]:
    """
    Yield Fibonacci numbers lazily with O(1) memory footprint.

    Args:
        count (int): Number of Fibonacci numbers to yield.

    Yields:
        int: Consecutive Fibonacci numbers.

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


def square_odd_numbers_loop(limit: int = 10) -> list[tuple[int, int]]:
    """
    Compute squares for odd integers in the range [0, limit - 1].

    Args:
        limit (int): Upper bound limit (exclusive).

    Returns:
        list[tuple[int, int]]: List of (odd_number, square_value) tuples.

    """
    odd_squares: list[tuple[int, int]] = []
    for num in range(limit):
        square = num**2
        if num % 2 == 0:
            continue
        odd_squares.append((num, square))
    return odd_squares


if __name__ == "__main__":
    print("--- 1. Perfect Numbers ---")
    print(f"Is 28 perfect? {is_perfect_number(28)}")
    print(f"Perfect numbers up to 10,000: {find_perfect_numbers_in_range(1, 10000)}")

    print("\n--- 2. Digit Difference ---")
    print(f"Digit difference for 213 (321 - 123): {digit_difference(213)}")

    print("\n--- 3. Fibonacci Sequence ---")
    print(f"First 10 terms: {fibonacci_iterative(10)}")

    print("\n--- 4. Odd Squares (0..9) ---")
    print(f"Odd squares: {square_odd_numbers_loop(10)}")
