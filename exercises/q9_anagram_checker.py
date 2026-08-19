"""
Exercise 9: Anagram Theory & Validator
======================================
Problem Statement:
What is an anagram and find if the two given strings are anagrams of each other.

Theoretical Definition:
An anagram is a word or phrase formed by rearranging the letters of a different
word or phrase, using all the original letters exactly once.
Examples:
- "listen" and "silent"
- "triangle" and "integral"
- "the eyes" and "they see"

Senior Engineering Highlights:
- Implements O(N) frequency counting via collections.Counter (or 26-char hash map).
- Sanitizes input: strips non-alphanumeric characters and normalizes case.
- Provides complete theoretical explanation string.
"""

from collections import Counter
import re
from typing import Tuple


def explain_anagram() -> str:
    """Returns a comprehensive theoretical explanation of what an anagram is."""
    return (
        "ANAGRAM DEFINITION:\n"
        "An anagram is a word or phrase created by rearranging all the letters of another\n"
        "word or phrase, utilizing every letter exactly once.\n\n"
        "Properties & Mathematical Foundation:\n"
        "1. Length Invariant: Both strings must contain the exact same total character count.\n"
        "2. Character Frequency Multi-set Invariant: The histogram of character frequencies\n"
        "   for both strings must be identical (i.e. Counter(S1) == Counter(S2)).\n"
        "3. Real-world Variations: Spaces and punctuation are conventionally ignored,\n"
        "   and comparisons are typically case-insensitive (e.g., 'Dormitory' == 'Dirty room')."
    )


def sanitize_string(s: str) -> str:
    """Removes non-alphanumeric characters and converts to lowercase."""
    return re.sub(r"[^a-zA-Z0-9]", "", s).lower()


def is_anagram(str1: str, str2: str) -> bool:
    """
    Determines if two strings are anagrams of each other using an O(N) frequency map.

    Time Complexity: O(N) where N is the length of the strings.
    Space Complexity: O(K) where K is the number of distinct characters (<= 36 for alphanumeric).

    Args:
        str1: First input string.
        str2: Second input string.

    Returns:
        True if str1 and str2 are anagrams, False otherwise.

    Examples:
        >>> is_anagram("listen", "silent")
        True
        >>> is_anagram("Dormitory", "Dirty room")
        True
        >>> is_anagram("hello", "world")
        False
    """
    clean1 = sanitize_string(str1)
    clean2 = sanitize_string(str2)

    if len(clean1) != len(clean2):
        return False

    return Counter(clean1) == Counter(clean2)


def is_anagram_sorting(str1: str, str2: str) -> bool:
    """Alternative implementation using O(N log N) character sorting."""
    clean1 = sanitize_string(str1)
    clean2 = sanitize_string(str2)
    return sorted(clean1) == sorted(clean2)


if __name__ == "__main__":
    print(explain_anagram())
    print("\n--- Anagram Test Cases ---")

    pairs = [
        ("listen", "silent"),
        ("triangle", "integral"),
        ("Dormitory", "Dirty room"),
        ("Eleven plus two", "Twelve plus one"),
        ("Python", "Java"),
    ]

    for s1, s2 in pairs:
        result = is_anagram(s1, s2)
        print(f"'{s1}' vs '{s2}' -> Is Anagram: {result}")
