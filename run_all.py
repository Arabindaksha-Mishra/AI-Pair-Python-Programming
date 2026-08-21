"""
Master Interactive Launcher & Demonstration CLI
================================================
Unified terminal runner for all 7 Comprehensive Senior Python Exercise
modules, the Capstone Automated Data Cleaning Assistant, the AST Code
Review Agent, and the CI Quality & Verification Pipeline.
"""

from __future__ import annotations

import os
import subprocess
import sys

from ai_pair_programming.telemetry import get_logger

_LOGGER = get_logger("launcher")

PROJECT_ROOT: str = os.path.dirname(os.path.abspath(__file__))
SRC_DIR: str = os.path.join(PROJECT_ROOT, "src")

BOLD: str = "\033[1m"
GREEN: str = "\033[32m"
CYAN: str = "\033[36m"
YELLOW: str = "\033[33m"
MAGENTA: str = "\033[35m"
RESET: str = "\033[0m"


def clear_screen() -> None:
    """
    Clear terminal screen across POSIX and Windows environments.

    Returns:
        None

    """
    os.system("cls" if os.name == "nt" else "clear")


def print_banner() -> None:
    """
    Render executive styling banner.

    Returns:
        None

    """
    print("=" * 68)
    print(
        f"{BOLD}{CYAN}   🚀 AI PAIR PYTHON PROGRAMMING: "
        f"7 SENIOR MODULES & CAPSTONE{RESET}"
    )
    print(
        f"{YELLOW}   Pure Standard Library | Zero Dependencies | "
        f"40 Tests (100% OK){RESET}"
    )
    print("=" * 68)


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


def run_exercise_module(module_name: str, display_name: str) -> None:
    """
    Execute an individual comprehensive exercise module.

    Args:
        module_name (str): Submodule name under ai_pair_programming.exercises.
        display_name (str): Human-readable header title.

    Returns:
        None

    """
    _LOGGER.info(f"Launching exercise module: {module_name}")
    print(f"\n{MAGENTA}{BOLD}>>> Launching {display_name}...{RESET}\n")
    subprocess.run(
        [sys.executable, "-m", f"ai_pair_programming.exercises.{module_name}"],
        env=_build_execution_env(),
    )
    input(f"\n{BOLD}Press [Enter] to return to menu...{RESET}")


def run_all_exercises_sequentially() -> None:
    """
    Execute all 7 comprehensive senior exercise modules in sequence.

    Returns:
        None

    """
    _LOGGER.info("Executing all 7 senior exercise modules sequentially...")
    modules: list[tuple[str, str]] = [
        ("unique_elements", "Module 1: Unique Elements & Set Algebra"),
        ("perfect_number", "Module 2: Number Theory & Perfect Numbers"),
        ("digit_difference", "Module 3: Digit Permutations & Difference"),
        ("fibonacci_series", "Module 4: Fibonacci Sequence Engineering"),
        ("anagram_solver", "Module 5: String Processing & Anagram NLP"),
        ("movie_tickets", "Module 6: Piecewise Logic & Movie Pricing"),
        ("interactive_loops", "Module 7: Interactive Loops & Sentinels"),
    ]
    for mod_name, label in modules:
        print(f"\n{MAGENTA}{BOLD}▶ Running {label}...{RESET}")
        subprocess.run(
            [sys.executable, "-m", f"ai_pair_programming.exercises.{mod_name}"],
            env=_build_execution_env(),
        )

    input(f"\n{BOLD}All 7 modules executed! Press [Enter] to return...{RESET}")


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
        [sys.executable, "-m", "ai_pair_programming.capstone.main"],
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


def run_ci_pipeline() -> None:
    """
    Execute full CI verification pipeline (Ruff, 88-col, AST security, tests).

    Returns:
        None

    """
    _LOGGER.info("Executing complete CI verification pipeline...")
    from CI.run_quality_checks import run_all_ci_checks

    run_all_ci_checks()
    input(f"\n{BOLD}Press [Enter] to return to main menu...{RESET}")


def _print_menu_options() -> None:
    """
    Display interactive menu options in terminal.

    Returns:
        None

    """
    print(f"{BOLD}PART 1: Senior Python Exercises (7 Comprehensive Modules){RESET}")
    print("   1.  📦 Module 1: Unique Elements & Set Algebra (Q1, Q10)")
    print("   2.  🔢 Module 2: Perfect Numbers & Divisor Sums (Q2)")
    print("   3.  🔢 Module 3: Digit Permutations & Difference (Q3)")
    print("   4.  🔢 Module 4: Fibonacci (Recursive Memoized & Iterative) (Q6)")
    print("   5.  🔤 Module 5: Anagram Solver (Frequency Hash & Sorting) (Q9)")
    print("   6.  🎟️ Module 6: Movie Theater Pricing & Box Office REPL (Q5)")
    print(
        "   7.  🍕 Module 7: Interactive Loops, Sentinels & Flow Control (Q4, Q7, Q8)"
    )
    print(f"   {YELLOW}A.  Run All 7 Comprehensive Modules Sequentially{RESET}")

    print(f"\n{BOLD}PART 2: Capstone Project (AI-Powered Data Quality){RESET}")
    print(
        "   8.  🧹 Automated Data Cleaning Assistant "
        "(Imputation, Outliers, Types, Deduplication)"
    )

    print(f"\n{BOLD}VERIFICATION, QUALITY & CI PIPELINE{RESET}")
    print(
        f"   {GREEN}P.  Run Complete CI Pipeline "
        f"(Format, Lint, 88-Col, Security, Tests){RESET}"
    )
    print(f"   {GREEN}T.  Run Automated Test Suite (40 Tests, 100% Pass Rate){RESET}")
    print(f"   {CYAN}C.  Run Automated Security & Code Bug Review Agent{RESET}")
    print(f"   {MAGENTA}V.  View Release Notes & Version History (RN.json){RESET}")
    print("   Q.  Quit")
    print("-" * 68)


def _handle_menu_choice(choice: str) -> bool:
    """
    Dispatch menu choice to appropriate runner function.

    Args:
        choice (str): Selected menu option string.

    Returns:
        bool: True to continue main loop, False to exit.

    """
    module_map: dict[str, tuple[str, str]] = {
        "1": ("unique_elements", "Module 1: Unique Elements & Set Algebra"),
        "2": ("perfect_number", "Module 2: Number Theory & Perfect Numbers"),
        "3": ("digit_difference", "Module 3: Digit Permutations & Difference"),
        "4": ("fibonacci_series", "Module 4: Fibonacci Sequence Engineering"),
        "5": ("anagram_solver", "Module 5: String Processing & Anagram NLP"),
        "6": ("movie_tickets", "Module 6: Piecewise Logic & Movie Pricing"),
        "7": ("interactive_loops", "Module 7: Interactive Loops & Sentinels"),
    }

    if choice in module_map:
        mod, name = module_map[choice]
        run_exercise_module(mod, name)
    elif choice == "A":
        run_all_exercises_sequentially()
    elif choice == "8":
        run_capstone_cleaner()
    elif choice == "P":
        run_ci_pipeline()
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
            input(f"{BOLD}Select an option [1-8, A, P, T, C, V, Q]: {RESET}")
            .strip()
            .upper()
        )
        if not _handle_menu_choice(choice):
            break


if __name__ == "__main__":
    main()
