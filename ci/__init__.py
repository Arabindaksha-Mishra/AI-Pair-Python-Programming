"""
CI & Quality Automation Suite
==============================
Modular verification tools for format auditing, line length enforcement,
schema validation, and continuous integration pipeline automation.
"""

from __future__ import annotations

from .check_line_length import audit_line_lengths
from .validate_release_notes import validate_rn_file

__all__ = [
    "audit_line_lengths",
    "validate_rn_file",
]
