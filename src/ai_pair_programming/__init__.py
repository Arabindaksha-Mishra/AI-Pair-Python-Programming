"""
AI Pair Python Programming Package
==================================
Standard library engineering suite organized into functional domain groups:
- algorithms        : Functional algorithms (Collections, Math, Strings, Loops)
- data_cleaner      : AI-Powered Tabular Data Cleaning Assistant
- data_transformer  : Reusable sanitization, imputation & outlier engine
- telemetry         : Structured Logging and 1-hour Rotating File Handlers
- tools             : AST Security Reviewer and Version Management Utilities
"""

from __future__ import annotations

from .telemetry.output_handler import (
    OutputHandler,
    get_logger,
    get_logs_directory,
)

__version__ = "2.0.0"
__all__ = [
    "OutputHandler",
    "__version__",
    "get_logger",
    "get_logs_directory",
]
