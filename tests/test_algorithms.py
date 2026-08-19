"""
Test Suite: Senior Python Algorithm & Domain Groups
===================================================
Unit tests covering algorithmic correctness, edge cases, and performance invariants:
- Group 1: Collections & Set Algebra (algorithms/collections_ops.py)
- Group 2: Numerical Mathematics (algorithms/numeric_math.py)
- Group 3: String Processing & NLP (algorithms/string_utils.py)
- Group 4: Interactive Loops (algorithms/interactive_loops.py)
"""

from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from ai_pair_programming.algorithms.collections_ops import (
    get_unique_elements,
    merge_sets_unique,
    symmetric_difference_unique,
)
from ai_pair_programming.algorithms.interactive_loops import (
    calculate_ticket_price,
    process_topping,
    simulate_pizza_toppings,
    simulate_ticket_pricing,
)
from ai_pair_programming.algorithms.numeric_math import (
    digit_difference,
    fibonacci_generator,
    fibonacci_iterative,
    fibonacci_recursive,
    find_perfect_numbers_in_range,
    is_perfect_number,
    square_odd_numbers_loop,
)
from ai_pair_programming.algorithms.string_utils import (
    generate_pizza_statements,
    is_anagram,
    is_anagram_sorting,
)


class TestSeniorAlgorithms(unittest.TestCase):
    """Unit tests organized across the 4 functional domain modules."""

    def test_collections_unique_elements(self) -> None:
        """
        Verify insertion-order preserved deduplication with fallbacks.

        Returns:
            None

        """
        self.assertEqual(get_unique_elements([1, 2, 2, 3, 4, 4, 1]), [1, 2, 3, 4])
        self.assertEqual(get_unique_elements(["a", "b", "a", "c"]), ["a", "b", "c"])
        self.assertEqual(get_unique_elements([]), [])
        self.assertEqual(get_unique_elements([[1, 2], [3], [1, 2]]), [[1, 2], [3]])

    def test_collections_set_operations(self) -> None:
        """
        Verify union and symmetric difference set operations.

        Returns:
            None

        """
        s1 = {1, 2, 3, 4}
        s2 = {3, 4, 5, 6}
        self.assertEqual(merge_sets_unique(s1, s2), {1, 2, 3, 4, 5, 6})
        self.assertEqual(symmetric_difference_unique(s1, s2), {1, 2, 5, 6})
        self.assertEqual(merge_sets_unique({1, 2}, {3, 4}), {1, 2, 3, 4})
        self.assertEqual(symmetric_difference_unique({1, 2}, {3, 4}), {1, 2, 3, 4})

    def test_math_perfect_number(self) -> None:
        """
        Verify O(sqrt(N)) perfect number evaluation and range filtering.

        Returns:
            None

        """
        self.assertTrue(is_perfect_number(6))
        self.assertTrue(is_perfect_number(28))
        self.assertTrue(is_perfect_number(496))
        self.assertTrue(is_perfect_number(8128))
        self.assertFalse(is_perfect_number(12))
        self.assertFalse(is_perfect_number(1))
        self.assertFalse(is_perfect_number(0))
        self.assertFalse(is_perfect_number(-28))
        self.assertEqual(find_perfect_numbers_in_range(1, 30), [6, 28])

    def test_math_digit_difference(self) -> None:
        """
        Verify calculation of difference between permutation extrema.

        Returns:
            None

        """
        self.assertEqual(digit_difference("213"), 198)
        self.assertEqual(digit_difference(213), 198)
        self.assertEqual(digit_difference("204"), 396)
        with self.assertRaises(ValueError):
            digit_difference("abc")

    def test_math_fibonacci(self) -> None:
        """
        Verify recursive memoized, iterative, and lazy generator Fibonacci.

        Returns:
            None

        """
        expected_10 = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        self.assertEqual(fibonacci_recursive(10), expected_10)
        self.assertEqual(fibonacci_iterative(10), expected_10)
        self.assertEqual(list(fibonacci_generator(10)), expected_10)
        self.assertEqual(fibonacci_recursive(0), [])
        self.assertEqual(fibonacci_iterative(1), [0])

    def test_math_square_odd_loop(self) -> None:
        """
        Verify parity filtered odd squares computation.

        Returns:
            None

        """
        squares = square_odd_numbers_loop(limit=10)
        expected = [(1, 1), (3, 9), (5, 25), (7, 49), (9, 81)]
        self.assertEqual(squares, expected)

    def test_strings_pizza_statements(self) -> None:
        """
        Verify pizza list formatting and summary paragraph templating.

        Returns:
            None

        """
        custom = ["Margherita", "Hawaiian", "Four Cheese"]
        names, stmts, summary = generate_pizza_statements(custom)
        self.assertEqual(names, custom)
        self.assertEqual(len(stmts), 3)
        self.assertEqual(stmts[0], "I like Margherita pizza.")
        self.assertIn("I really love pizza!", summary)

    def test_strings_anagram_checker(self) -> None:
        """
        Verify O(N) frequency and O(N log N) sorting anagram detection.

        Returns:
            None

        """
        self.assertTrue(is_anagram("listen", "silent"))
        self.assertTrue(is_anagram("Dormitory", "Dirty room"))
        self.assertTrue(is_anagram("Eleven plus two", "Twelve plus one"))
        self.assertFalse(is_anagram("hello", "world"))
        self.assertFalse(is_anagram("abc", "abcd"))
        self.assertTrue(is_anagram_sorting("listen", "silent"))

    def test_loops_pizza_toppings(self) -> None:
        """
        Verify sentinel loop parsing and headless simulation.

        Returns:
            None

        """
        inputs = ["mushrooms", "cheese", "quit", "olives"]
        res = simulate_pizza_toppings(inputs)
        self.assertEqual(
            res,
            ["I'll add mushrooms to your pizza!", "I'll add cheese to your pizza!"],
        )
        self.assertIsNone(process_topping("quit"))
        self.assertIsNone(process_topping(""))

    def test_loops_movie_ticket_pricing(self) -> None:
        """
        Verify tiered box office ticket pricing calculation and simulation.

        Returns:
            None

        """
        self.assertEqual(calculate_ticket_price(2), 0)
        self.assertEqual(calculate_ticket_price(3), 10)
        self.assertEqual(calculate_ticket_price(12), 10)
        self.assertEqual(calculate_ticket_price(13), 15)
        self.assertEqual(calculate_ticket_price(65), 15)
        with self.assertRaises(ValueError):
            calculate_ticket_price(-1)

        sim_res = simulate_ticket_pricing([2, 5, 20, "quit"])
        self.assertEqual(len(sim_res), 3)
        self.assertEqual(sim_res[0][1], 0)
        self.assertEqual(sim_res[1][1], 10)
        self.assertEqual(sim_res[2][1], 15)


if __name__ == "__main__":
    unittest.main(verbosity=2)
