"""
CI Utility: Line Length Auditor
===============================
Validates that all source code and documentation files adhere strictly to
the 88-column maximum width limit.
"""

from __future__ import annotations

import os
import sys

MAX_LINE_LENGTH: int = 88
EXCLUDED_DIRECTORIES: set[str] = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    ".ruff_cache",
    "logs",
    "dist",
    "build",
}
EXCLUDED_EXTENSIONS: set[str] = {
    ".zip",
    ".png",
    ".jpg",
    ".jpeg",
    ".ico",
    ".gif",
}


def audit_line_lengths(root_dir: str = ".") -> list[tuple[str, int, int]]:
    """
    Scan all non-excluded files for lines exceeding MAX_LINE_LENGTH.

    Args:
        root_dir (str): Root filesystem path to start traversal.

    Returns:
        list[tuple[str, int, int]]: Violations (path, line_number, length).

    """
    violations: list[tuple[str, int, int]] = []

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRECTORIES]
        for file_name in files:
            _, ext = os.path.splitext(file_name)
            if ext.lower() in EXCLUDED_EXTENSIONS:
                continue

            file_path = os.path.join(root, file_name)
            with open(file_path, encoding="utf-8", errors="replace") as f:
                for line_idx, line in enumerate(f, 1):
                    line_content = line.rstrip("\r\n")
                    if len(line_content) > MAX_LINE_LENGTH:
                        violations.append((file_path, line_idx, len(line_content)))

    return violations


def main() -> None:
    """
    CLI entrypoint for line length validation in CI.

    Returns:
        None

    """
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    violations = audit_line_lengths(root)

    if violations:
        print(
            f"❌ Line Length Failure: Found {len(violations)} lines "
            f"exceeding {MAX_LINE_LENGTH} columns:"
        )
        for path, line_no, length in violations:
            print(f"  • {path}:{line_no} (length={length})")
        sys.exit(1)

    print(f"✅ Line length audit passed: all files <= {MAX_LINE_LENGTH} columns.")
    sys.exit(0)


if __name__ == "__main__":
    main()
