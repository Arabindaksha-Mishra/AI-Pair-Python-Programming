#!/usr/bin/env python3
"""
AI Pair Python Programming — Master Interactive Launcher
=========================================================
Single unified entrypoint organized by functional domain modules:
1. Collections & Set Algebra (Unique elements, Set operations)
2. Numerical Mathematics & Sequences (Perfect numbers, Fibonacci, Squares)
3. String Processing & NLP Utilities (Anagram solver, Pizza statements)
4. Interactive Loops & Flow Control (Pizza toppings sentinel, Ticket pricing)
5. Capstone Project: AI-Powered Data Cleaning Assistant
T. Automated Unit Test Suite
C. Automated Security & Code Bug Review Agent
V. Release Notes & Version Management (RN.json)

Usage:
    python3 run_all.py
"""

from __future__ import annotations

import os
import subprocess
import sys

from ai_pair_programming.output_handler import get_logger

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

_LOGGER = get_logger("launcher")

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"


def clear_screen() -> None:
    """
    Clear terminal screen across Unix and Windows platforms.

    Returns:
        None

    """
    os.system("cls" if os.name == "nt" else "clear")


def print_banner() -> None:
    """
    Render application header banner in terminal.

    Returns:
        None

    """
    print(f"{CYAN}{BOLD}")
    print("=" * 68)
    print("      🚀 AI PAIR PYTHON PROGRAMMING — SENIOR CAPSTONE SUITE       ")
    print("=" * 68)
    print(
        f"{RESET}{GREEN}• uv / src Standard Architecture  |  "
        f"100% Python Standard Library{RESET}\n"
    )


def _build_execution_env() -> dict[str, str]:
    """
    Prepare child process environment with src directory on PYTHONPATH.

    Returns:
        dict[str, str]: Environment variable mapping.

    """
    env = os.environ.copy()
    env["PYTHONPATH"] = SRC_DIR + (
        os.pathsep + env["PYTHONPATH"] if "PYTHONPATH" in env else ""
    )
    return env


def run_domain_module(module_name: str, display_name: str) -> None:
    """
    Execute a standalone algorithm domain group.

    Args:
        module_name (str): Suffix of algorithms module to run.
        display_name (str): Human-readable header title.

    Returns:
        None

    """
    _LOGGER.info(f"Launching domain module: {module_name}")
    print(f"\n{MAGENTA}{BOLD}>>> Launching {display_name}...{RESET}\n")
    subprocess.run(
        [sys.executable, "-m", f"ai_pair_programming.algorithms.{module_name}"],
        env=_build_execution_env(),
    )
    input(f"\n{BOLD}Press [Enter] to return to menu...{RESET}")


def run_capstone_cleaner() -> None:
    """
    Execute interactive data cleaner CLI application.

    Returns:
        None

    """
    _LOGGER.info("Launching Capstone Data Cleaning Assistant CLI...")
    print(
        f"\n{CYAN}{BOLD}>>> Launching Capstone: "
        f"Automated Data Cleaning Assistant...{RESET}\n"
    )
    subprocess.run(
        [sys.executable, "-m", "ai_pair_programming.data_cleaner.main"],
        env=_build_execution_env(),
    )
    input(f"\n{BOLD}Press [Enter] to return to menu...{RESET}")


def run_tests() -> None:
    """
    Execute full automated unit test suite.

    Returns:
        None

    """
    _LOGGER.info("Executing automated unit test suite...")
    print(f"\n{YELLOW}{BOLD}>>> Running Automated Unit Test Suite...{RESET}\n")
    from test_suite import run_all_tests

    run_all_tests()
    input(f"\n{BOLD}Press [Enter] to return to main menu...{RESET}")


def run_code_review() -> None:
    """
    Run automated security and AST code review agent.

    Returns:
        None

    """
    _LOGGER.info("Launching Automated AST Security & Defect Review Agent...")
    print(
        f"\n{CYAN}{BOLD}>>> Launching Automated Security & "
        f"Code Bug Review Agent...{RESET}\n"
    )
    from ai_pair_programming.tools.code_review_agent import CodeReviewAgent

    agent = CodeReviewAgent(root_dir=PROJECT_ROOT)
    agent.scan_directory(PROJECT_ROOT)
    report = agent.generate_report()
    print(report)
    input(f"\n{BOLD}Press [Enter] to return to main menu...{RESET}")


def run_version_manager() -> None:
    """
    Display release notes and version management history from RN.json.

    Returns:
        None

    """
    _LOGGER.info("Displaying Release Notes (RN.json) history...")
    from ai_pair_programming.tools.version_manager import VersionManager

    vm = VersionManager()
    print(vm.format_history())
    input(f"\n{BOLD}Press [Enter] to return to main menu...{RESET}")


def _print_menu_options() -> None:
    """
    Display interactive menu options in terminal.

    Returns:
        None

    """
    print(f"{BOLD}PART 1: Senior Python Exercises (Domain Groups){RESET}")
    print(
        "  1.  📦 Collections & Sets       : Unique Elements (Q1), "
        "Set Union & Diff (Q10)"
    )
    print(
        "  2.  🔢 Numerical Math & Series  : Perfect Numbers (Q2), "
        "Digit Diff (Q3), Fibonacci (Q6), Squares (Q8)"
    )
    print(
        "  3.  🔤 String Processing & NLP  : Anagram Solver (Q9), Pizza Statements (Q7)"
    )
    print(
        "  4.  🔄 Interactive Loops & REPL : Pizza Toppings (Q4), "
        "Movie Ticket Pricing (Q5)"
    )
    print(f"\n{BOLD}PART 2: Capstone Project (AI-Powered Data Quality){RESET}")
    print(
        "  5.  🧹 Automated Data Cleaning Assistant "
        "(Imputation, Outliers, Types, Deduplication)"
    )
    print(f"\n{BOLD}VERIFICATION, QUALITY & VERSION MANAGEMENT{RESET}")
    print(f"  {GREEN}T.  Run Automated Test Suite (35+ Tests, 100% Pass Rate){RESET}")
    print(f"  {CYAN}C.  Run Automated Security & Code Bug Review Agent{RESET}")
    print(f"  {MAGENTA}V.  View Release Notes & Version History (RN.json){RESET}")
    print("  Q.  Quit")
    print("-" * 68)


def _handle_menu_choice(choice: str) -> bool:
    """
    Dispatch menu choice to appropriate runner function.

    Args:
        choice (str): Selected menu option string.

    Returns:
        bool: True to continue main loop, False to exit.

    """
    if choice == "1":
        run_domain_module("collections_ops", "Group 1: Collections & Set Algebra")
    elif choice == "2":
        run_domain_module("numeric_math", "Group 2: Numerical Mathematics & Sequences")
    elif choice == "3":
        run_domain_module("string_utils", "Group 3: String Processing & NLP Utilities")
    elif choice == "4":
        run_domain_module(
            "interactive_loops", "Group 4: Interactive Loops & Flow Control"
        )
    elif choice == "5":
        run_capstone_cleaner()
    elif choice == "T":
        run_tests()
    elif choice == "C":
        run_code_review()
    elif choice == "V":
        run_version_manager()
    elif choice in ("Q", "QUIT", "EXIT"):
        print(f"\n{CYAN}Thank you for evaluating this submission! Goodbye.{RESET}\n")
        return False
    return True


def main() -> None:
    """
    Execute master interactive menu loop.

    Returns:
        None

    """
    while True:
        clear_screen()
        print_banner()
        _print_menu_options()
        choice = (
            input(f"{BOLD}Select an option [1-5, T, C, V, Q]: {RESET}").strip().upper()
        )
        if not _handle_menu_choice(choice):
            break


if __name__ == "__main__":
    main()
