"""
Exercise 7: Favorite Pizza List, Statements, and Summary
========================================================
Problem Statement:
1. Think of at least three kinds of favorite pizza. Store these pizza names in a list.
2. Use a for loop to print the name of each pizza.
3. Modify the for loop to print a sentence: "I like {pizza} pizza."
4. Add concluding lines outside the loop stating how much you like pizza (3-4 lines total).

Senior Engineering Highlights:
- Clean list iteration and f-string templating.
- Separation of formatting logic into testable helper functions.
"""

from typing import List, Tuple


def get_default_pizzas() -> List[str]:
    """Returns a list of curated favorite pizzas."""
    return ["Margherita", "Pepperoni", "Truffle Mushroom", "BBQ Chicken"]


def format_pizza_names(pizzas: List[str]) -> List[str]:
    """Formats just the names of pizzas."""
    return [pizza for pizza in pizzas]


def format_pizza_statements(pizzas: List[str]) -> List[str]:
    """Formats full sentences for each pizza."""
    return [f"I like {pizza} pizza." for pizza in pizzas]


def generate_pizza_statements(pizzas: List[str] = None) -> Tuple[List[str], List[str], str]:
    """
    Executes the complete pizza progression:
    - Step 1: Raw names
    - Step 2: Individual liking statements
    - Step 3: Concluding summary paragraph

    Returns:
        Tuple containing (names_list, statements_list, concluding_summary)
    """
    if pizzas is None:
        pizzas = get_default_pizzas()

    names = [p for p in pizzas]
    statements = [f"I like {p} pizza." for p in pizzas]
    concluding_summary = (
        "Pizza is hands down one of my all-time favorite foods.\n"
        "The crispy crust paired with rich tomato sauce and melted cheese is unmatched.\n"
        "Whether it's a simple Margherita or loaded toppings, I really love pizza!"
    )

    return names, statements, concluding_summary


def display_pizza_progression() -> None:
    """Prints formatted output for all 3 requirements."""
    pizzas = get_default_pizzas()
    names, statements, conclusion = generate_pizza_statements(pizzas)

    print("--- Step 1: Printing Pizza Names ---")
    for name in names:
        print(f"• {name}")

    print("\n--- Step 2: Printing Pizza Sentences ---")
    for sentence in statements:
        print(sentence)

    print("\n--- Step 3: Concluding Pizza Statement ---")
    print(conclusion)


if __name__ == "__main__":
    display_pizza_progression()
