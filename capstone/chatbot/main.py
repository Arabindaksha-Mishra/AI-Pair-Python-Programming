"""
Interactive Terminal Entrypoint for Task 1: Rule-Based Chatbot
==============================================================
Provides an interactive command-line loop with ANSI styling and session export.
"""

import sys
from capstone.chatbot.bot_engine import RuleBasedChatbot


def run_chatbot_cli() -> None:
    bot = RuleBasedChatbot()

    print("\n" + "=" * 60)
    print("   🤖 Context-Aware Rule-Based Python Chatbot (Built-in Only)   ")
    print("=" * 60)
    print("Type 'help' for options, or 'exit' / 'quit' to end the session.\n")

    initial_greeting = bot.process_message("hello")
    print(f"Bot: {initial_greeting}\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nSession terminated by user.")
            break

        if not user_input:
            continue

        response = bot.process_message(user_input)
        print(f"\nBot: {response}\n")

        # Check if conversation ended
        if bot.context.last_intent == "farewell":
            break

    print("-" * 60)
    print(f"Session ended. Total turns: {bot.context.turn_count}")
    if bot.context.user_name:
        print(f"User remembered: {bot.context.user_name}")
    print("-" * 60 + "\n")


if __name__ == "__main__":
    run_chatbot_cli()
