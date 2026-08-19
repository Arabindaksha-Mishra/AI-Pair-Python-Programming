"""
Exercise 8: Number Squaring with Modulo Parity and Continue Control Flow
========================================================================
Problem Statement:
Define a loop that iterates over all numbers 0 through 9, and squares each number.
Within this loop, at each iteration, check if the number is divisible by 2,
at which point the loop will continue to execute; otherwise print the output.

Mechanism:
- For even numbers (0, 2, 4, 6, 8): num % 2 == 0 -> triggers 'continue', skipping print.
- For odd numbers (1, 3, 5, 7, 9): prints the number and its square (1, 9, 25, 49, 81).
"""

from typing import List, Tuple


def square_odd_numbers_loop(limit: int = 10, verbose: bool = True) -> List[Tuple[int, int]]:
    """
    Iterates from 0 up to limit - 1, squares each number, and prints/returns
    only the odd numbers using `continue` for even numbers.

    Args:
        limit: Upper bound (exclusive), default is 10 (0..9).
        verbose: If True, prints formatted console output.

    Returns:
        List of tuples: (odd_number, squared_value)
    """
    odd_squares: List[Tuple[int, int]] = []

    for num in range(limit):
        square = num ** 2

        # If number is divisible by 2, continue to next iteration
        if num % 2 == 0:
            continue

        # Executed only when num is not divisible by 2 (i.e. odd numbers)
        odd_squares.append((num, square))
        if verbose:
            print(f"Number: {num} -> Square: {square}")

    return odd_squares


if __name__ == "__main__":
    print("--- Squaring Numbers (0 to 9) with 'continue' on Even Numbers ---")
    results = square_odd_numbers_loop(10, verbose=True)
    print("\nSummary of Processed (Odd) Squares:", results)
