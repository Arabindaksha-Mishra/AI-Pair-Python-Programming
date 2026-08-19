"""
Package Level CLI Entrypoint
============================
Redirects to the master interactive launcher.
"""

from __future__ import annotations

import os
import sys

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def main() -> None:
    """
    Delegate execution to the master CLI interactive runner.

    Returns:
        None

    """
    import run_all

    run_all.main()


if __name__ == "__main__":
    main()
