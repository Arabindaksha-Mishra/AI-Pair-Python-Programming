"""
Module 5: String Processing & Anagram NLP Engine (Python 3.12+)
================================================================
Comprehensive dual-mode implementations for anagram verification:
1. O(N) Character Frequency Hash Table Verification (Q9)
2. O(N log N) Canonical Sorted Form Verification (Q9)
"""

from __future__ import annotations

from collections import Counter


def explain_anagram() -> str:
    """
    Return formal linguistic and algorithmic definition of an anagram.

    Returns:
        str: Multi-line conceptual explanation with real-world examples.

    """
    return (
        "An anagram is a word or phrase formed by rearranging the letters "
        "of a different word or phrase, typically using all the original "
        "letters exactly once.\n"
        "Algorithmic Characterization:\n"
        "• Two strings are anagrams iff their character frequency histograms "
        "are identical after whitespace and case normalization.\n"
        "• Examples: 'listen' <-> 'silent', 'Debit Card' <-> 'Bad Credit'."
    )


def are_anagrams_frequency(str1: str, str2: str) -> bool:
    """
    Determine anagram equivalence using O(N) character frequency hashing.

    Normalizes inputs by stripping whitespace and converting to lowercase.

    Args:
        str1 (str): First candidate string.
        str2 (str): Second candidate string.

    Returns:
        bool: True if str1 and str2 are valid anagrams, False otherwise.

    """
    clean1 = [c for c in str1.lower() if not c.isspace()]
    clean2 = [c for c in str2.lower() if not c.isspace()]

    if len(clean1) != len(clean2):
        return False

    return Counter(clean1) == Counter(clean2)


def are_anagrams_sorted(str1: str, str2: str) -> bool:
    """
    Determine anagram equivalence using O(N log N) canonical string sorting.

    Args:
        str1 (str): First candidate string.
        str2 (str): Second candidate string.

    Returns:
        bool: True if sorted character arrays match exactly, False otherwise.

    """
    clean1 = [c for c in str1.lower() if not c.isspace()]
    clean2 = [c for c in str2.lower() if not c.isspace()]

    return sorted(clean1) == sorted(clean2)


def main() -> None:
    """
    Demonstrate Module 5 anagram checking algorithms.

    Returns:
        None

    """
    print("==================================================================")
    print("   🔤 MODULE 5: ANAGRAM SOLVER (FREQUENCY & SORTING)              ")
    print("==================================================================")
    print(explain_anagram())
    print("\nBenchmark Test Pairs:")
    pairs = [
        ("listen", "silent"),
        ("Debit Card", "Bad Credit"),
        ("astronomer", "moon starer"),
        ("python", "java"),
        ("hello", "world"),
        ("Dormitory", "Dirty Room"),
    ]
    for s1, s2 in pairs:
        freq_res = are_anagrams_frequency(s1, s2)
        sort_res = are_anagrams_sorted(s1, s2)
        status = "✅ ANAGRAMS" if freq_res else "❌ NOT ANAGRAMS"
        print(f"'{s1}' vs '{s2}' -> {status} (Freq: {freq_res}, Sort: {sort_res})")
    print("==================================================================\n")


if __name__ == "__main__":
    main()
