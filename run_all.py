#!/usr/bin/env python3
"""
AI Pair Python Programming — Master Interactive Launcher
=========================================================
Single unified entrypoint for trainers & reviewers to evaluate all exercises
and capstone modules with zero configuration.

Usage:
    python3 run_all.py
"""

import os
import sys
import subprocess
import unittest

# Colors for terminal styling
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    print(f"{CYAN}{BOLD}")
    print("=" * 68)
    print("      🚀 AI PAIR PYTHON PROGRAMMING — SENIOR CAPSTONE SUITE       ")
    print("=" * 68)
    print(f"{RESET}{GREEN}• 100% Python Standard Library  |  0 External Dependencies  |  0 API Keys{RESET}\n")


def run_tests():
    print(f"\n{YELLOW}{BOLD}>>> Running Automated Unit Test Suite...{RESET}\n")
    loader = unittest.TestLoader()
    suite = loader.discover(".", pattern="test_suite.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    input(f"\n{BOLD}Press [Enter] to return to main menu...{RESET}")


def run_exercise(module_name: str, display_name: str):
    print(f"\n{MAGENTA}{BOLD}>>> Launching {display_name}...{RESET}\n")
    subprocess.run([sys.executable, "-m", f"exercises.{module_name}"])
    input(f"\n{BOLD}Press [Enter] to return to menu...{RESET}")


def run_capstone_chatbot():
    print(f"\n{CYAN}{BOLD}>>> Launching Task 1: Context-Aware Rule-Based Chatbot...{RESET}\n")
    subprocess.run([sys.executable, "-m", "capstone.chatbot.main"])
    input(f"\n{BOLD}Press [Enter] to return to menu...{RESET}")


def run_capstone_cleaner():
    print(f"\n{CYAN}{BOLD}>>> Launching Task 2: Automated Data Cleaning Assistant...{RESET}\n")
    subprocess.run([sys.executable, "-m", "capstone.data_cleaner.main"])
    input(f"\n{BOLD}Press [Enter] to return to menu...{RESET}")


def main():
    while True:
        clear_screen()
        print_banner()
        print(f"{BOLD}PART 1: Senior Python Exercises (Built-in Libraries Only){RESET}")
        print("  1.  Q1: Unique Elements (Preserving Order)")
        print("  2.  Q2: Perfect Number Validator (O(sqrt(N)))")
        print("  3.  Q3: Digit Permutation Extrema Difference (e.g. 213 -> 198)")
        print("  4.  Q4: Pizza Toppings Interactive Sentinel Loop ('quit')")
        print("  5.  Q5: Movie Theater Ticket Pricing Loop (Age-tiered)")
        print("  6.  Q6: Fibonacci Series (Recursive vs Iterative vs Generator)")
        print("  7.  Q7: Favorite Pizza List & Sentence Summary")
        print("  8.  Q8: Square Numbers (0..9) with Parity 'continue'")
        print("  9.  Q9: Anagram Theory & O(N) Frequency Checker")
        print("  10. Q10: Set Operations & Duplicate Elimination (Union / Symm Diff)")
        print(f"\n{BOLD}PART 2: Capstone Projects{RESET}")
        print("  11. Task 1: Context-Aware Rule-Based Chatbot (Regex & State Memory)")
        print("  12. Task 2: Automated Data Cleaning Assistant (Dirty Datasets)")
        print(f"\n{BOLD}VERIFICATION & UTILITIES{RESET}")
        print(f"  {GREEN}T.  Run Automated Test Suite (100% Coverage){RESET}")
        print("  Q.  Quit")
        print("-" * 68)

        choice = input(f"{BOLD}Select an option [1-12, T, Q]: {RESET}").strip().upper()

        if choice == "1":
            run_exercise("q1_unique_elements", "Q1: Unique Elements")
        elif choice == "2":
            run_exercise("q2_perfect_number", "Q2: Perfect Number")
        elif choice == "3":
            run_exercise("q3_digit_difference", "Q3: Digit Difference")
        elif choice == "4":
            run_exercise("q4_pizza_toppings", "Q4: Pizza Toppings Loop")
        elif choice == "5":
            run_exercise("q5_movie_ticket", "Q5: Movie Ticket Pricing")
        elif choice == "6":
            run_exercise("q6_fibonacci", "Q6: Fibonacci Comparison")
        elif choice == "7":
            run_exercise("q7_pizza_statements", "Q7: Pizza Statements")
        elif choice == "8":
            run_exercise("q8_square_loop", "Q8: Square Loop with Continue")
        elif choice == "9":
            run_exercise("q9_anagram_checker", "Q9: Anagram Checker")
        elif choice == "10":
            run_exercise("q10_set_operations", "Q10: Set Operations")
        elif choice == "11":
            run_capstone_chatbot()
        elif choice == "12":
            run_capstone_cleaner()
        elif choice == "T":
            run_tests()
        elif choice in ("Q", "QUIT", "EXIT"):
            print(f"\n{CYAN}Thank you for evaluating this submission! Goodbye.{RESET}\n")
            break


if __name__ == "__main__":
    main()
