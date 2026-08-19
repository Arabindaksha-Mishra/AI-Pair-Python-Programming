"""
Domain Group 4: Interactive Loops & Flow Control (Python 3.12+)
================================================================
Covers:
1. Pizza Toppings Interactive Prompt Loop with 'quit' Sentinel (Q4)
2. Movie Theater Ticket Pricing Loop (<3: Free, 3..12: $10, >12: $15) (Q5)

100% Python Standard Library (Zero external dependencies).
"""

from collections.abc import Iterable

from ai_pair_programming.telemetry import get_logger

_LOGGER = get_logger("algorithms.loops")

INFANT_AGE_THRESHOLD = 3
CHILD_AGE_THRESHOLD = 12
FREE_TICKET_PRICE = 0
CHILD_TICKET_PRICE = 10
ADULT_TICKET_PRICE = 15


def process_topping(topping_input: str) -> str | None:
    """
    Process a single pizza topping input and generate confirmation message.

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


if __name__ == "__main__":
    print("--- 1. Pizza Toppings Simulation ---")
    print(simulate_pizza_toppings(["mushrooms", "olives", "quit"]))

    print("\n--- 2. Movie Ticket Pricing Simulation ---")
    for age_val, cost, msg in simulate_ticket_pricing([2, 8, 25]):
        print(f"Age {age_val:2d} -> ${cost:2d} | {msg}")
