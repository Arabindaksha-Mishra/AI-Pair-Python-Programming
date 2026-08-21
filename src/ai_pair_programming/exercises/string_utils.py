"""
Domain Group 3: String Processing & NLP (Python 3.12+)
========================================================
Covers:
1. Anagram Solvers (Frequency Counter & Canonical Sort) (Q9)
2. Pizza Statement Formatting (Q7)
"""

from __future__ import annotations

from collections import Counter


def is_anagram(s1: str, s2: str) -> bool:
    """Check if two strings are anagrams using character frequency counting."""
    c1 = Counter(ch.lower() for ch in s1 if ch.isalnum())
    c2 = Counter(ch.lower() for ch in s2 if ch.isalnum())
    return c1 == c2


def is_anagram_sorting(s1: str, s2: str) -> bool:
    """Check if two strings are anagrams using canonical sorting."""
    norm1 = sorted(ch.lower() for ch in s1 if ch.isalnum())
    norm2 = sorted(ch.lower() for ch in s2 if ch.isalnum())
    return norm1 == norm2


def generate_pizza_statements(
    pizza_types: list[str],
) -> tuple[list[str], list[str], str]:
    """
    Format a list of pizza types into itemized appreciation statements and summary.

    Returns:
        tuple[list[str], list[str], str]: (names, statements, summary_paragraph)
    """
    stmts = [f"I like {p.strip()} pizza." for p in pizza_types]
    summary = (
        "I really love pizza! Whether it is thin crust, deep dish, or wood-fired "
        "artisan style, pizza is my absolute favorite food."
    )
    return pizza_types, stmts, summary
