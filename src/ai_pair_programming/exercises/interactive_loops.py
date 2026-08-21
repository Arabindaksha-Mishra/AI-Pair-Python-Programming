"""
Module 7: Interactive Loops, Sentinels & Flow Control (Python 3.12+)
====================================================================
Comprehensive implementations for:
1. Sentinel-Controlled Interactive REPL Loop (Q4: Pizza Toppings)
2. Age-Tiered Ticket Pricing & Box Office REPL (Q5: Movie Tickets)
3. List Iteration & Narrative Summary Templating (Q7: Pizza Statements)
4. Modulo Branch Filtering with Continue Statement (Q8: Odd Squares)
"""

from __future__ import annotations

from collections.abc import Iterable
import sys
from typing import TextIO

INFANT_AGE_THRESHOLD: int = 3
CHILD_AGE_THRESHOLD: int = 12

FREE_TICKET_PRICE: int = 0
CHILD_TICKET_PRICE: int = 10
ADULT_TICKET_PRICE: int = 15


def process_topping(topping_input: str) -> str | None:
    """
    Validate and format a topping input, returning None on termination sentinels.

    Args:
        topping_input (str): Raw topping name entered by user.

    Returns:
        str | None: Confirmation message or None if input matches quit sentinel.

    """
    cleaned = topping_input.strip()
    if cleaned.lower() in ("quit", "exit", "q") or not cleaned:
        return None
    return f"I'll add {cleaned} to your pizza!"


def simulate_pizza_toppings(inputs: Iterable[str]) -> list[str]:
    """
    Simulate pizza topping entry loop headlessly for automated testing.

    Args:
        inputs (Iterable[str]): Sequence of simulated topping inputs.

    Returns:
        list[str]: Output messages generated until termination.

    """
    messages: list[str] = []
    for item in inputs:
        msg = process_topping(item)
        if msg is None and item.strip().lower() in ("quit", "exit", "q"):
            break
        elif msg is not None:
            messages.append(msg)
    return messages


def pizza_toppings_interactive() -> list[str]:
    """
    Execute interactive CLI loop prompting user for pizza toppings.

    Returns:
        list[str]: List of toppings successfully added by the user.

    """
    print("\n--- Custom Pizza Builder ---")
    print("Enter toppings (type 'quit' to finish):\n")
    added: list[str] = []
    while True:
        try:
            val = input("Please enter a topping: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nOrder cancelled.")
            break

        msg = process_topping(val)
        if msg is None and val.lower() in ("quit", "exit", "q"):
            print("\nFinishing your pizza order!")
            break
        elif msg is not None:
            print(msg)
            added.append(val)
    return added


def pizza_toppings_repl(
    input_stream: TextIO | None = None,
    output_stream: TextIO | None = None,
) -> list[str]:
    """
    Execute sentinel-controlled REPL for accumulating pizza toppings.

    Args:
        input_stream (TextIO | None): Source stream for user inputs.
        output_stream (TextIO | None): Destination stream for output.

    Returns:
        list[str]: Sequence of added toppings excluding sentinel.

    """
    in_stream = input_stream if input_stream is not None else sys.stdin
    out_stream = output_stream if output_stream is not None else sys.stdout

    toppings: list[str] = []
    out_stream.write("--- Pizza Topping Customizer (Enter 'quit' to finish) ---\n")

    while True:
        out_stream.write("Enter a pizza topping: ")
        out_stream.flush()
        line = in_stream.readline()
        if not line:
            break

        topping = line.strip()
        if not topping:
            continue

        if topping.lower() == "quit":
            out_stream.write("Finished adding toppings. Preparing your pizza!\n")
            break

        toppings.append(topping)
        out_stream.write(f"Adding {topping} to your pizza!\n")

    return toppings


def calculate_ticket_price(age: int) -> int:
    """
    Calculate theater ticket price based on viewer age tier.

    Args:
        age (int): Viewer age in years.

    Returns:
        int: Ticket cost in dollars (0, 10, or 15).

    Raises:
        ValueError: If age is negative.

    """
    if age < 0:
        raise ValueError(f"Age cannot be negative: {age}")
    if age < INFANT_AGE_THRESHOLD:
        return FREE_TICKET_PRICE
    elif age <= CHILD_AGE_THRESHOLD:
        return CHILD_TICKET_PRICE
    else:
        return ADULT_TICKET_PRICE


def format_ticket_cost(age: int) -> str:
    """
    Format ticket pricing message according to age.

    Args:
        age (int): Viewer age in years.

    Returns:
        str: Human-readable ticket pricing sentence.

    """
    price = calculate_ticket_price(age)
    return (
        "Your ticket is FREE!" if price == 0 else f"Your movie ticket cost is: ${price}"
    )


def simulate_ticket_pricing(
    age_inputs: Iterable[int | str],
) -> list[tuple[int, int, str]]:
    """
    Simulate batch box office calculations headlessly.

    Args:
        age_inputs (Iterable[int | str]): Sequence of ages or quit strings.

    Returns:
        list[tuple[int, int, str]]: List of (age, price, formatted_message).

    """
    results: list[tuple[int, int, str]] = []
    for item in age_inputs:
        if str(item).strip().lower() in ("quit", "exit", "q"):
            break
        try:
            age = int(item)
            results.append((age, calculate_ticket_price(age), format_ticket_cost(age)))
        except (ValueError, TypeError):
            continue
    return results


def movie_ticket_pricing_loop() -> None:
    """
    Run interactive box office CLI loop computing group ticket totals.

    Returns:
        None

    """
    print("\n--- Movie Theater Box Office ---")
    print(
        "Pricing: Under 3 = Free | Ages 3-12 = $10 | Over 12 = $15 "
        "(type 'quit' to exit)\n"
    )
    total_tickets = 0
    total_revenue = 0
    while True:
        try:
            user_input = input("Enter viewer age (or 'quit'): ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if user_input.lower() in ("quit", "exit", "q"):
            print(f"\nTotal tickets: {total_tickets} | Total cost: ${total_revenue}")
            break
        try:
            age = int(user_input)
            price = calculate_ticket_price(age)
            total_tickets += 1
            total_revenue += price
            print(f"-> {format_ticket_cost(age)}")
        except ValueError:
            print("Invalid input. Please enter a valid integer age.")


def format_pizza_statements(pizza_types: list[str]) -> str:
    """
    Format a multi-line narrative of pizza preferences and concluding summary.

    Args:
        pizza_types (list[str]): Names of preferred pizza varieties.

    Returns:
        str: Multi-line aggregated text containing itemized statements
             and concluding appreciation summary.

    Raises:
        ValueError: If pizza_types list is empty.

    """
    if not pizza_types:
        raise ValueError("Pizza types list cannot be empty.")

    lines: list[str] = []
    for pizza in pizza_types:
        lines.append(f"I like {pizza.strip()} pizza.")

    lines.append(
        "I really love pizza! Whether it is thin crust, deep dish, or "
        "wood-fired artisan style, pizza is my absolute favorite food."
    )
    return "\n".join(lines)


def square_even_continue_loop(
    limit: int = 10, output_stream: TextIO | None = None
) -> list[int]:
    """
    Compute squares of numbers 0 through limit-1, skipping even numbers.

    Evaluates (i % 2 == 0) with a continue statement, outputting formatted
    squared values only for odd integers.

    Args:
        limit (int): Upper non-inclusive iteration bound (default 10).
        output_stream (TextIO | None): Destination stream for print output.

    Returns:
        list[int]: Computed squares of odd numbers that executed past continue.

    """
    out = output_stream if output_stream is not None else sys.stdout
    odd_squares: list[int] = []

    for i in range(limit):
        if i % 2 == 0:
            continue

        sq = i**2
        odd_squares.append(sq)
        out.write(f"Odd number {i} squared is: {sq}\n")

    return odd_squares


def main() -> None:
    """
    Demonstrate Module 7 interactive loops and flow control algorithms.

    Returns:
        None

    """
    print("==================================================================")
    print("   🍕 MODULE 7: INTERACTIVE LOOPS, SENTINELS & FLOW CONTROL       ")
    print("==================================================================")
    print("1. Demonstration of Modulo Filter & Continue Statement (0-9):")
    squares = square_even_continue_loop()
    print(f"Generated Odd Squares: {squares}")

    print("\n2. Demonstration of Narrative Pizza Templating:")
    sample_pizzas = ["Pepperoni", "Margherita", "BBQ Chicken"]
    print(format_pizza_statements(sample_pizzas))
    print("==================================================================\n")


if __name__ == "__main__":
    main()
