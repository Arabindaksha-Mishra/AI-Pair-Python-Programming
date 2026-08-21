"""
Module 6: Piecewise Business Logic & Movie Pricing REPL (Python 3.12+)
=======================================================================
Comprehensive implementation of age-tiered theater ticket pricing (Q5):
- Under age 3       : Free ($0)
- Between 3 and 12  : $10
- Over age 12       : $15
"""

from __future__ import annotations

import sys
from typing import TextIO


def calculate_movie_ticket_price(age: int) -> int:
    """
    Calculate movie ticket admission cost according to strict age tiers.

    Args:
        age (int): Customer age in completed years.

    Returns:
        int: Admission price in USD (0, 10, or 15).

    Raises:
        ValueError: If age is negative or non-numeric.

    """
    if not isinstance(age, int) or age < 0:
        raise ValueError(f"Age must be a non-negative integer, received: {age!r}")

    if age < 3:
        return 0
    if 3 <= age <= 12:
        return 10
    return 15


def movie_tickets_repl(
    input_stream: TextIO | None = None,
    output_stream: TextIO | None = None,
) -> None:
    """
    Interactive terminal REPL prompt for evaluating ticket prices.

    Args:
        input_stream (TextIO | None): Input source stream.
        output_stream (TextIO | None): Destination stream.

    Returns:
        None

    """
    in_stream = input_stream if input_stream is not None else sys.stdin
    out_stream = output_stream if output_stream is not None else sys.stdout

    out_stream.write("--- Movie Ticket Box Office (Enter 'quit' to exit) ---\n")

    while True:
        out_stream.write("Please enter your age: ")
        out_stream.flush()
        line = in_stream.readline()
        if not line:
            break

        cleaned = line.strip()
        if not cleaned:
            continue

        if cleaned.lower() == "quit":
            out_stream.write("Thank you for visiting the cinema!\n")
            break

        try:
            age_val = int(cleaned)
            price = calculate_movie_ticket_price(age_val)
            if price == 0:
                out_stream.write("Your ticket is FREE!\n")
            else:
                out_stream.write(f"The cost of your movie ticket is ${price}.\n")
        except ValueError:
            out_stream.write("Invalid age input. Please enter a positive integer.\n")


def main() -> None:
    """
    Demonstrate Module 6 movie theater ticket pricing.

    Returns:
        None

    """
    print("==================================================================")
    print("   🎟️  MODULE 6: MOVIE THEATER TICKET PRICING & BOX OFFICE REPL   ")
    print("==================================================================")
    sample_ages = [1, 2, 3, 7, 12, 13, 25, 65]
    for age in sample_ages:
        cost = calculate_movie_ticket_price(age)
        print(f"Customer Age: {age:>2} years -> Ticket Cost: ${cost}")
    print("==================================================================\n")


if __name__ == "__main__":
    main()
