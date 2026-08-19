"""
Exercise 5: Movie Theater Ticket Pricing Loop
=============================================
Problem Statement:
A movie theater charges different ticket prices depending on a person’s age:
- Under 3: Free ($0)
- Between 3 and 12 (inclusive): $10
- Over 12: $15
Write a loop in which you ask users their age, and then tell them the cost of their movie ticket.

Senior Engineering Highlights:
- Separation of pricing business logic (pure function) from I/O loop.
- Robust exception handling for non-integer inputs.
- Testable headless batch evaluation + interactive loop.
"""

from typing import Iterable, List, Tuple, Union


def calculate_ticket_price(age: int) -> int:
    """
    Computes ticket price based on age category.

    Args:
        age: Customer age (non-negative integer).

    Returns:
        Cost in dollars: 0 for <3, 10 for 3..12, 15 for >12.

    Raises:
        ValueError: If age is negative.
    """
    if age < 0:
        raise ValueError(f"Age cannot be negative: {age}")

    if age < 3:
        return 0
    elif 3 <= age <= 12:
        return 10
    else:
        return 15


def format_ticket_cost(age: int) -> str:
    """Returns human-readable pricing string."""
    price = calculate_ticket_price(age)
    if price == 0:
        return "Your ticket is FREE!"
    return f"Your movie ticket cost is: ${price}"


def simulate_ticket_pricing(age_inputs: Iterable[Union[int, str]]) -> List[Tuple[int, int, str]]:
    """
    Batch simulator for automated testing.
    Returns: List of (age, price, formatted_message)
    """
    results: List[Tuple[int, int, str]] = []
    for item in age_inputs:
        if str(item).strip().lower() in ("quit", "exit", "q"):
            break
        try:
            age = int(item)
            price = calculate_ticket_price(age)
            msg = format_ticket_cost(age)
            results.append((age, price, msg))
        except (ValueError, TypeError):
            continue
    return results


def movie_ticket_pricing_loop() -> None:
    """Interactive CLI loop for box office ticket calculations."""
    print("\n--- Movie Theater Box Office ---")
    print("Pricing tiers: Under 3 = Free | Ages 3-12 = $10 | Over 12 = $15")
    print("Enter 'quit' to exit.\n")

    total_tickets = 0
    total_revenue = 0

    while True:
        try:
            user_input = input("Enter viewer age (or 'quit'): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting ticketing system.")
            break

        if user_input.lower() in ("quit", "exit", "q"):
            print("\n--- Order Summary ---")
            print(f"Total tickets: {total_tickets}")
            print(f"Total cost: ${total_revenue}")
            break

        try:
            age = int(user_input)
            price = calculate_ticket_price(age)
            total_tickets += 1
            total_revenue += price
            print(f"-> {format_ticket_cost(age)}")
        except ValueError as err:
            print(f"Invalid input: {err}. Please enter a positive integer age.")


if __name__ == "__main__":
    test_ages = [2, 3, 7, 12, 13, 25, 65]
    print("--- Batch Pricing Simulation ---")
    for age_val, cost, text in simulate_ticket_pricing(test_ages):
        print(f"Age {age_val:2d} -> Price: ${cost:2d} | Message: {text}")
