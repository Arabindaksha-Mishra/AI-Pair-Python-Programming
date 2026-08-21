"""
Part 1: Senior Python Exercises Package (Python 3.12+)
======================================================
Comprehensive implementations for the 7 Senior Python Exercise modules:
- Exercise 1: unique_elements.py   (Order-preserved deduplication & set algebra)
- Exercise 2: perfect_number.py    (Square-root divisor summation & range search)
- Exercise 3: digit_difference.py  (Digit permutation max-min analysis)
- Exercise 4: fibonacci_series.py  (Memoized recursive & iterative sequence)
- Exercise 5: anagram_solver.py    (NLP character frequency & canonical sort)
- Exercise 6: movie_tickets.py     (Age-tiered pricing & box office REPL)
- Exercise 7: interactive_loops.py (Sentinel REPL, templating & modulo skip)

100% Pure Standard Library (Zero External Dependencies).
"""

from __future__ import annotations

from .anagram_solver import (
    are_anagrams_frequency,
    are_anagrams_sorted,
    explain_anagram,
)
from .digit_difference import (
    digit_difference,
    get_digit_extremes,
)
from .fibonacci_series import (
    fibonacci_generator,
    fibonacci_iterative,
    fibonacci_recursive,
)
from .interactive_loops import (
    format_pizza_statements,
    pizza_toppings_repl,
    square_even_continue_loop,
)
from .movie_tickets import (
    calculate_movie_ticket_price,
    movie_tickets_repl,
)
from .perfect_number import (
    find_perfect_numbers_in_range,
    is_perfect_number,
)
from .unique_elements import (
    set_union_and_difference,
    unique_elements,
)

__all__ = [
    "are_anagrams_frequency",
    "are_anagrams_sorted",
    "calculate_movie_ticket_price",
    "digit_difference",
    "explain_anagram",
    "fibonacci_generator",
    "fibonacci_iterative",
    "fibonacci_recursive",
    "find_perfect_numbers_in_range",
    "format_pizza_statements",
    "get_digit_extremes",
    "is_perfect_number",
    "movie_tickets_repl",
    "pizza_toppings_repl",
    "set_union_and_difference",
    "square_even_continue_loop",
    "unique_elements",
]
