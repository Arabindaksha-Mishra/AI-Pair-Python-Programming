"""
Exercise 3: Digit Permutation Extrema Difference
================================================
Problem Statement:
Write a function that accepts a number as a parameter. The function should return
a number that’s the difference between the largest and smallest numbers that the digits
can form in the number.

Example:
Input: "213"
Largest form: 321
Smallest form: 123
Difference: 321 - 123 = 198

Senior Engineering Highlights:
- Accepts integer, float, or string representations.
- Handles digits with zeros properly (e.g., '204' -> max: 420, min: 024 -> 24; diff = 396).
- Resilient to whitespace and negative signs.
"""

from typing import Union


def digit_difference(number_input: Union[int, str, float], return_as_string: bool = False) -> Union[int, str]:
    """
    Computes the difference between the largest and smallest numbers that can be
    formed from the digits of the input.

    Args:
        number_input: An integer or string containing digits (e.g. 213 or "213").
        return_as_string: If True, returns the result as a string, otherwise as int.

    Returns:
        The numerical difference (or string formatted result).

    Raises:
        ValueError: If no valid digits are found in input.

    Examples:
        >>> digit_difference("213")
        198
        >>> digit_difference(213)
        198
        >>> digit_difference("204")
        396
    """
    # Extract only digit characters (stripping minus signs, decimals, or whitespace)
    raw_str = str(number_input)
    digits = [ch for ch in raw_str if ch.isdigit()]

    if not digits:
        raise ValueError(f"No numerical digits found in input: {number_input!r}")

    # Largest number: sort digits in descending order
    descending_digits = sorted(digits, reverse=True)
    largest_num = int("".join(descending_digits))

    # Smallest number: sort digits in ascending order
    ascending_digits = sorted(digits)
    smallest_num = int("".join(ascending_digits))

    diff = largest_num - smallest_num

    return str(diff) if return_as_string else diff


if __name__ == "__main__":
    test_values = ["213", 213, "204", "9081", "-523", 7]
    print("--- Digit Difference Calculator ---")
    for val in test_values:
        result = digit_difference(val)
        print(f"Input: {str(val):6s} -> Difference: {result}")
