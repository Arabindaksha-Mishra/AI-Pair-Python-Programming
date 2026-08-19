"""
Test Suite: Part 1 — Senior Python Exercises (Q1 to Q10)
=========================================================
Unit tests covering algorithmic correctness, edge cases, and performance invariants.
"""

import unittest
import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exercises.q1_unique_elements import get_unique_elements
from exercises.q2_perfect_number import is_perfect_number, find_perfect_numbers_in_range
from exercises.q3_digit_difference import digit_difference
from exercises.q4_pizza_toppings import process_topping, simulate_pizza_toppings
from exercises.q5_movie_ticket import calculate_ticket_price, simulate_ticket_pricing
from exercises.q6_fibonacci import fibonacci_recursive, fibonacci_iterative, fibonacci_generator
from exercises.q7_pizza_statements import generate_pizza_statements
from exercises.q8_square_loop import square_odd_numbers_loop
from exercises.q9_anagram_checker import is_anagram, is_anagram_sorting
from exercises.q10_set_operations import merge_sets_unique, symmetric_difference_unique


class TestSeniorExercises(unittest.TestCase):
    """Unit tests for all 10 Python Senior Exercises."""

    def test_q1_unique_elements(self):
        self.assertEqual(get_unique_elements([1, 2, 2, 3, 4, 4, 1]), [1, 2, 3, 4])
        self.assertEqual(get_unique_elements(["a", "b", "a", "c"]), ["a", "b", "c"])
        self.assertEqual(get_unique_elements([]), [])
        # Test unhashable nested items fallback
        self.assertEqual(get_unique_elements([[1, 2], [3], [1, 2]]), [[1, 2], [3]])

    def test_q2_perfect_number(self):
        self.assertTrue(is_perfect_number(6))
        self.assertTrue(is_perfect_number(28))
        self.assertTrue(is_perfect_number(496))
        self.assertTrue(is_perfect_number(8128))
        self.assertFalse(is_perfect_number(12))
        self.assertFalse(is_perfect_number(1))
        self.assertFalse(is_perfect_number(0))
        self.assertFalse(is_perfect_number(-28))
        self.assertEqual(find_perfect_numbers_in_range(1, 30), [6, 28])

    def test_q3_digit_difference(self):
        # "213" -> 321 - 123 = 198
        self.assertEqual(digit_difference("213"), 198)
        self.assertEqual(digit_difference(213), 198)
        # "204" -> 420 - 24 = 396
        self.assertEqual(digit_difference("204"), 396)
        with self.assertRaises(ValueError):
            digit_difference("abc")

    def test_q4_pizza_toppings(self):
        inputs = ["mushrooms", "cheese", "quit", "olives"]
        res = simulate_pizza_toppings(inputs)
        self.assertEqual(
            res,
            ["I'll add mushrooms to your pizza!", "I'll add cheese to your pizza!"],
        )

    def test_q5_movie_ticket_pricing(self):
        self.assertEqual(calculate_ticket_price(0), 0)
        self.assertEqual(calculate_ticket_price(2), 0)
        self.assertEqual(calculate_ticket_price(3), 10)
        self.assertEqual(calculate_ticket_price(12), 10)
        self.assertEqual(calculate_ticket_price(13), 15)
        self.assertEqual(calculate_ticket_price(65), 15)
        with self.assertRaises(ValueError):
            calculate_ticket_price(-5)

    def test_q6_fibonacci(self):
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        self.assertEqual(fibonacci_recursive(10), expected)
        self.assertEqual(fibonacci_iterative(10), expected)
        self.assertEqual(list(fibonacci_generator(10)), expected)
        self.assertEqual(fibonacci_iterative(0), [])
        self.assertEqual(fibonacci_iterative(1), [0])

    def test_q7_pizza_statements(self):
        pizzas = ["Margherita", "Pepperoni"]
        names, stmts, concl = generate_pizza_statements(pizzas)
        self.assertEqual(names, ["Margherita", "Pepperoni"])
        self.assertEqual(stmts, ["I like Margherita pizza.", "I like Pepperoni pizza."])
        self.assertIn("favorite", concl.lower())

    def test_q8_square_odd_loop(self):
        res = square_odd_numbers_loop(10, verbose=False)
        expected = [(1, 1), (3, 9), (5, 25), (7, 49), (9, 81)]
        self.assertEqual(res, expected)

    def test_q9_anagram_checker(self):
        self.assertTrue(is_anagram("listen", "silent"))
        self.assertTrue(is_anagram("Dormitory", "Dirty room"))
        self.assertTrue(is_anagram_sorting("listen", "silent"))
        self.assertFalse(is_anagram("hello", "world"))

    def test_q10_set_operations(self):
        s1 = {1, 2, 3}
        s2 = {3, 4, 5}
        self.assertEqual(merge_sets_unique(s1, s2), {1, 2, 3, 4, 5})
        self.assertEqual(symmetric_difference_unique(s1, s2), {1, 2, 4, 5})


if __name__ == "__main__":
    unittest.main(verbosity=2)
