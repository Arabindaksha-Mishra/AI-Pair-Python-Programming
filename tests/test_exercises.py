"""
Test Suite: Task 1 — Senior Python Exercises
===================================================
Unit tests covering algorithmic correctness, edge cases, and performance invariants:
- Group 1: Collections & Set Algebra (exercises/collections_ops.py)
- Group 2: Numerical Mathematics (exercises/numeric_math.py)
- Group 3: String Processing & NLP (exercises/string_utils.py)
- Group 4: Interactive Loops (exercises/interactive_loops.py)
"""

from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from ai_pair_programming.exercises.collections_ops import (
    get_unique_elements,
    merge_sets_unique,
    symmetric_difference_unique,
)
from ai_pair_programming.exercises.interactive_loops import (
    calculate_ticket_price,
    process_topping,
    simulate_pizza_toppings,
    simulate_ticket_pricing,
)
from ai_pair_programming.exercises.numeric_math import (
    digit_difference,
    fibonacci_generator,
    fibonacci_iterative,
    fibonacci_recursive,
    find_perfect_numbers_in_range,
    is_perfect_number,
    square_odd_numbers_loop,
)
from ai_pair_programming.exercises.string_utils import (
    generate_pizza_statements,
    is_anagram,
    is_anagram_sorting,
)


class TestSeniorExercises(unittest.TestCase):
    """Unit tests for Task 1: Senior Python Exercises."""

    def test_collections_unique_elements(self) -> None:
        """Verify insertion-order preserved deduplication."""
        self.assertEqual(get_unique_elements([1, 2, 2, 3, 4, 4, 1]), [1, 2, 3, 4])
        self.assertEqual(get_unique_elements(["a", "b", "a", "c"]), ["a", "b", "c"])
        self.assertEqual(get_unique_elements([]), [])

    def test_collections_set_algebra(self) -> None:
        """Verify union and symmetric difference set operations."""
        set_a = {1, 2, 3, 4}
        set_b = {3, 4, 5, 6}
        self.assertEqual(merge_sets_unique(set_a, set_b), {1, 2, 3, 4, 5, 6})
        self.assertEqual(symmetric_difference_unique(set_a, set_b), {1, 2, 5, 6})

    def test_math_perfect_numbers(self) -> None:
        """Verify square-root limit perfect number detection."""
        self.assertTrue(is_perfect_number(6))
        self.assertTrue(is_perfect_number(28))
        self.assertTrue(is_perfect_number(496))
        self.assertFalse(is_perfect_number(12))
        self.assertEqual(find_perfect_numbers_in_range(1, 500), [6, 28, 496])

    def test_math_digit_difference(self) -> None:
        """Verify calculation of difference between permutation extrema."""
        self.assertEqual(digit_difference("213"), 198)
        self.assertEqual(digit_difference(213), 198)
        self.assertEqual(digit_difference("204"), 396)
        with self.assertRaises(ValueError):
            digit_difference("abc")

    def test_math_fibonacci(self) -> None:
        """Verify recursive memoized, iterative, and generator Fibonacci."""
        expected_10 = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        self.assertEqual(fibonacci_recursive(10), expected_10)
        self.assertEqual(fibonacci_iterative(10), expected_10)
        self.assertEqual(list(fibonacci_generator(10)), expected_10)
        self.assertEqual(fibonacci_recursive(0), [])
        self.assertEqual(fibonacci_iterative(1), [0])

    def test_math_square_odd_loop(self) -> None:
        """Verify parity filtered odd squares computation."""
        squares = square_odd_numbers_loop(limit=10)
        expected = [(1, 1), (3, 9), (5, 25), (7, 49), (9, 81)]
        self.assertEqual(squares, expected)

    def test_strings_pizza_statements(self) -> None:
        """Verify pizza list formatting and summary paragraph templating."""
        custom = ["Margherita", "Hawaiian", "Four Cheese"]
        names, stmts, summary = generate_pizza_statements(custom)
        self.assertEqual(names, custom)
        self.assertEqual(len(stmts), 3)
        self.assertEqual(stmts[0], "I like Margherita pizza.")
        self.assertIn("I really love pizza!", summary)

    def test_strings_anagram_checker(self) -> None:
        """Verify frequency and sorting anagram detection."""
        self.assertTrue(is_anagram("Listen", "Silent"))
        self.assertTrue(is_anagram_sorting("Triangle", "Integral"))
        self.assertFalse(is_anagram("Hello", "World"))
        self.assertFalse(is_anagram_sorting("Python", "Java"))

    def test_loops_sentinel_toppings(self) -> None:
        """Verify topping validation and sentinel processing."""
        self.assertIn("Pepperoni", process_topping("Pepperoni") or "")
        self.assertIsNone(process_topping("quit"))
        self.assertIsNone(process_topping(""))
        toppings = ["Mushroom", "Olives", "quit", "Pineapple"]
        results = simulate_pizza_toppings(toppings)
        self.assertEqual(len(results), 2)

    def test_loops_ticket_pricing(self) -> None:
        """Verify age-tiered ticket pricing logic."""
        self.assertEqual(calculate_ticket_price(2), 0)
        self.assertEqual(calculate_ticket_price(10), 10)
        ages = [2, 10, 30]
        results = simulate_ticket_pricing(ages)
        prices = [res[1] for res in results]
        self.assertEqual(prices, [0, 10, 15])
