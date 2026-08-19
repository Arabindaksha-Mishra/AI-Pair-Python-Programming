"""
Domain Group 3: String Processing & NLP Utilities
=================================================
Covers:
1. Anagram Definition & O(N) Character Frequency Checker (Q9)
2. Pizza Statement Construction & Summary Paragraph Templating (Q7)

100% Python Standard Library (collections, re).
"""

from __future__ import annotations

from collections import Counter
import re

from ai_pair_programming.output_handler import get_logger

_LOGGER = get_logger("algorithms.strings")


def explain_anagram() -> str:
    """
    Provide theoretical explanation and mathematical properties of anagrams.

    Returns:
        str: Comprehensive multi-line explanation of anagram principles.

    """
    return (
        "ANAGRAM DEFINITION:\n"
        "An anagram is a word or phrase formed by rearranging all the letters\n"
        "of another word or phrase, utilizing every letter exactly once.\n\n"
        "Properties & Mathematical Foundation:\n"
        "1. Length Invariant: Both strings must contain the exact same count.\n"
        "2. Multi-set Invariant: The histogram of character frequencies matches.\n"
        "3. Case/Punctuation Invariant: Spaces and punctuation are ignored."
    )


def sanitize_string(s: str) -> str:
    """
    Strip non-alphanumeric characters and lowercase string for comparison.

    Args:
        s (str): Raw input string.

    Returns:
        str: Normalized lowercase alphanumeric string.

    """
    return re.sub(r"[^a-zA-Z0-9]", "", s).lower()


def is_anagram(str1: str, str2: str) -> bool:
    """
    Determine if two strings are anagrams using O(N) frequency counts.

    Args:
        str1 (str): First string to compare.
        str2 (str): Second string to compare.

    Returns:
        bool: True if str1 and str2 are anagrams, False otherwise.

    """
    clean1 = sanitize_string(str1)
    clean2 = sanitize_string(str2)

    if len(clean1) != len(clean2):
        return False

    return Counter(clean1) == Counter(clean2)


def is_anagram_sorting(str1: str, str2: str) -> bool:
    """
    Determine if two strings are anagrams using O(N log N) character sorting.

    Args:
        str1 (str): First string to compare.
        str2 (str): Second string to compare.

    Returns:
        bool: True if str1 and str2 are anagrams, False otherwise.

    """
    clean1 = sanitize_string(str1)
    clean2 = sanitize_string(str2)
    return sorted(clean1) == sorted(clean2)


def get_default_pizzas() -> list[str]:
    """
    Provide default list of sample pizzas.

    Returns:
        list[str]: Default favorite pizza names.

    """
    return ["Margherita", "Pepperoni", "Truffle Mushroom", "BBQ Chicken"]


def format_pizza_names(pizzas: list[str]) -> list[str]:
    """
    Format raw pizza names into a standardized list.

    Args:
        pizzas (list[str]): List of pizza names.

    Returns:
        list[str]: Copy of pizza names.

    """
    return list(pizzas)


def format_pizza_statements(pizzas: list[str]) -> list[str]:
    """
    Construct expressive sentence statements for each pizza.

    Args:
        pizzas (list[str]): List of pizza names.

    Returns:
        list[str]: Formatted liking statements.

    """
    return [f"I like {pizza} pizza." for pizza in pizzas]


def generate_pizza_statements(
    pizzas: list[str] | None = None,
) -> tuple[list[str], list[str], str]:
    """
    Generate progressive pizza names, statements, and summary text.

    Args:
        pizzas (list[str] | None): Optional custom list of pizzas.

    Returns:
        tuple[list[str], list[str], str]: Tuple containing (names,
            formatted_statements, closing_summary_paragraph).

    """
    if pizzas is None:
        pizzas = get_default_pizzas()

    names = format_pizza_names(pizzas)
    statements = format_pizza_statements(pizzas)
    closing_statement = (
        f"From the authentic simplicity of {pizzas[0]} to the savory "
        f"richness of {pizzas[1]},\nevery style offers something special. "
        f"Gourmet options like {pizzas[2]} elevate the experience.\n"
        f"I really love pizza!"
    )
    return names, statements, closing_statement


if __name__ == "__main__":
    print("--- 1. Anagram Verification ---")
    print(f"'listen' vs 'silent': {is_anagram('listen', 'silent')}")
    print(f"'Dormitory' vs 'Dirty room': {is_anagram('Dormitory', 'Dirty room')}")

    print("\n--- 2. Pizza Statements ---")
    _, stmts_list, summary = generate_pizza_statements()
    for stmt in stmts_list:
        print(f"• {stmt}")
    print(f"\nSummary:\n{summary}")
