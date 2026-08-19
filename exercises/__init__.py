"""
AI Pair Python Programming - Senior Engineer Exercises Package
==============================================================
All modules implemented using Python Standard Library only (zero external dependencies).
"""

from .q1_unique_elements import get_unique_elements, get_unique_elements_ordered
from .q2_perfect_number import is_perfect_number, find_perfect_numbers_in_range
from .q3_digit_difference import digit_difference
from .q4_pizza_toppings import pizza_toppings_interactive, simulate_pizza_toppings
from .q5_movie_ticket import calculate_ticket_price, movie_ticket_pricing_loop
from .q6_fibonacci import fibonacci_recursive, fibonacci_iterative, fibonacci_generator
from .q7_pizza_statements import generate_pizza_statements
from .q8_square_loop import square_odd_numbers_loop
from .q9_anagram_checker import is_anagram, explain_anagram
from .q10_set_operations import merge_sets_unique, symmetric_difference_unique

__all__ = [
    "get_unique_elements",
    "get_unique_elements_ordered",
    "is_perfect_number",
    "find_perfect_numbers_in_range",
    "digit_difference",
    "pizza_toppings_interactive",
    "simulate_pizza_toppings",
    "calculate_ticket_price",
    "movie_ticket_pricing_loop",
    "fibonacci_recursive",
    "fibonacci_iterative",
    "fibonacci_generator",
    "generate_pizza_statements",
    "square_odd_numbers_loop",
    "is_anagram",
    "explain_anagram",
    "merge_sets_unique",
    "symmetric_difference_unique",
]
