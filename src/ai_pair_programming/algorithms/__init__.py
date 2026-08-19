"""
Algorithms Domain Package (Python 3.12+)
========================================
Organized into 4 intuitive domain categories:
1. collections_ops   : Unique elements (Q1), Set operations (Q10)
2. numeric_math      : Perfect number (Q2), Digit diff (Q3), Fibonacci (Q6)
3. string_utils      : Pizza statements (Q7), Anagram checker (Q9)
4. interactive_loops : Pizza toppings sentinel (Q4), Movie ticket pricing (Q5)
"""

from .collections_ops import (
    get_unique_elements,
    merge_sets_unique,
    symmetric_difference_unique,
)
from .interactive_loops import (
    calculate_ticket_price,
    movie_ticket_pricing_loop,
    pizza_toppings_interactive,
    process_topping,
    simulate_pizza_toppings,
    simulate_ticket_pricing,
)
from .numeric_math import (
    digit_difference,
    fibonacci_generator,
    fibonacci_iterative,
    fibonacci_recursive,
    find_perfect_numbers_in_range,
    is_perfect_number,
    square_odd_numbers_loop,
)
from .string_utils import (
    explain_anagram,
    format_pizza_names,
    format_pizza_statements,
    generate_pizza_statements,
    get_default_pizzas,
    is_anagram,
    is_anagram_sorting,
    sanitize_string,
)

__all__ = [
    "calculate_ticket_price",
    "digit_difference",
    "explain_anagram",
    "fibonacci_generator",
    "fibonacci_iterative",
    "fibonacci_recursive",
    "find_perfect_numbers_in_range",
    "format_pizza_names",
    "format_pizza_statements",
    "generate_pizza_statements",
    "get_default_pizzas",
    "get_unique_elements",
    "is_anagram",
    "is_anagram_sorting",
    "is_perfect_number",
    "merge_sets_unique",
    "movie_ticket_pricing_loop",
    "pizza_toppings_interactive",
    "process_topping",
    "sanitize_string",
    "simulate_pizza_toppings",
    "simulate_ticket_pricing",
    "square_odd_numbers_loop",
    "symmetric_difference_unique",
]
