"""
CI Master Runner: Complete Quality & Verification Suite
========================================================
Executes all formatting, linting, line width, security review,
release notes, and test suite verification gates.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys


def _find_ruff_executable() -> str:
    """
    Locate ruff binary in PATH or user local bin directory.

    Returns:
        str: Executable command or path for ruff.

    """
    which_ruff = shutil.which("ruff")
    if which_ruff:
        return which_ruff

    local_ruff = os.path.expanduser("~/.local/bin/ruff")
    if os.path.isfile(local_ruff) and os.access(local_ruff, os.X_OK):
        return local_ruff

    return "ruff"


def _run_step(description: str, cmd: list[str]) -> bool:
    """
    Execute an individual verification step and print results.

    Args:
        description (str): Human-readable step label.
        cmd (list[str]): Command tokens to execute.

    Returns:
        bool: True if step passed with exit code 0, False otherwise.

    """
    print(f"\n▶ Running: {description}...")
    env = dict(os.environ)
    if "PYTHONPATH" not in env:
        env["PYTHONPATH"] = "src"
    else:
        env["PYTHONPATH"] = f"src:{env['PYTHONPATH']}"

    result = subprocess.run(cmd, env=env)
    if result.returncode == 0:
        print(f"  ✅ {description} PASSED")
        return True

    print(f"  ❌ {description} FAILED (exit code {result.returncode})")
    return False


def run_all_ci_checks() -> int:
    """
    Run complete sequence of CI verification gates.

    Returns:
        int: 0 if all gates passed, 1 if any gate failed.

    """
    print("==================================================================")
    print("      🚀 ENTERPRISE CI QUALITY & VERIFICATION PIPELINE           ")
    print("==================================================================")

    ruff_cmd = _find_ruff_executable()

    steps: list[tuple[str, list[str]]] = [
        (
            "Ruff Code Formatting Check",
            [ruff_cmd, "format", "--check", "."],
        ),
        (
            "Ruff Linter & Standards Check",
            [ruff_cmd, "check", "."],
        ),
        (
            "88-Column Line Width Validation",
            [sys.executable, "CI/check_line_length.py"],
        ),
        (
            "Release Notes (release_notes.json) Schema Validation",
            [sys.executable, "CI/validate_release_notes.py"],
        ),
        (
            "AST Security & Defect Review Agent",
            [
                sys.executable,
                "-m",
                "ai_pair_programming.tools.code_review_agent",
            ],
        ),
        (
            "Master Unit & Integration Test Suite (40 Tests)",
            [sys.executable, "tests.py"],
        ),
    ]

    failed_steps: list[str] = []
    for desc, command in steps:
        success = _run_step(desc, command)
        if not success:
            failed_steps.append(desc)

    print("\n==================================================================")
    if failed_steps:
        print(f"❌ CI PIPELINE FAILED: {len(failed_steps)} gate(s) failed:")
        for failed in failed_steps:
            print(f"  • {failed}")
        print("==================================================================\n")
        return 1

    print("✅ ALL CI GATES PASSED! Codebase is healthy and ready for merge/push.")
    print("==================================================================\n")
    return 0


def main() -> None:
    """
    CLI entrypoint for master CI checks.

    Returns:
        None

    """
    exit_code = run_all_ci_checks()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
