"""
Exercise 4: Pizza Toppings Interactive Prompt Loop
==================================================
Problem Statement:
Write a loop that prompts the user to enter a series of pizza toppings until they
enter a 'quit' value. As they enter each topping, print a message saying you’ll add
that topping to their pizza.

Senior Engineering Highlights:
- Dual interface: Interactive standard I/O loop + Headless simulator for automated unittesting.
- Case-insensitive sentinel handling ('quit', 'QUIT', 'exit').
- Sanitizes whitespace and rejects empty strings.
"""

from typing import Iterable, List, Optional


def process_topping(topping_input: str) -> Optional[str]:
    """
    Processes a single topping input.

    Returns:
        The message string if valid topping, None if sentinel 'quit' received.
    """
    cleaned = topping_input.strip()
    if cleaned.lower() in ("quit", "exit", "q"):
        return None
    if not cleaned:
        return None  # Skip empty submissions
    return f"I'll add {cleaned} to your pizza!"


def simulate_pizza_toppings(inputs: Iterable[str]) -> List[str]:
    """
    Headless simulator for automated test execution without blocking stdin.

    Args:
        inputs: An iterable sequence of user input strings.

    Returns:
        List of generated response messages until 'quit' is encountered.
    """
    messages: List[str] = []
    for item in inputs:
        msg = process_topping(item)
        if msg is None and item.strip().lower() in ("quit", "exit", "q"):
            break
        elif msg is not None:
            messages.append(msg)
    return messages


def pizza_toppings_interactive() -> List[str]:
    """Runs the interactive command-line loop prompting the user for toppings."""
    print("\n--- Custom Pizza Builder ---")
    print("Enter your favorite toppings (type 'quit' when finished):\n")

    added_toppings: List[str] = []
    prompt = "Please enter a topping: "

    while True:
        try:
            user_input = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print("\nOrder cancelled.")
            break

        msg = process_topping(user_input)
        if msg is None and user_input.strip().lower() in ("quit", "exit", "q"):
            print("\nFinishing your pizza order!")
            break
        elif msg is not None:
            print(msg)
            added_toppings.append(user_input.strip())

    return added_toppings


if __name__ == "__main__":
    # Test headless simulation
    sample_inputs = ["mushrooms", "extra cheese", "olives", "quit", "jalapenos"]
    print("--- Running Headless Simulation ---")
    simulated_output = simulate_pizza_toppings(sample_inputs)
    for line in simulated_output:
        print(line)
