"""
AI Pair Python Programming Package
==================================
Standard library engineering suite organized into functional domain groups:
- algorithms     : Functional algorithm modules (Collections, Math, Strings, Loops)
- data_cleaner   : AI-Powered Tabular Data Cleaning Assistant
- tools          : AST Security Reviewer and Distribution Utilities
- output_handler : Structured Logging and Pipeline Telemetry
"""

from __future__ import annotations

from .output_handler import OutputHandler, get_logger, get_logs_directory

__version__ = "2.0.0"
__all__ = [
    "OutputHandler",
    "__version__",
    "get_logger",
    "get_logs_directory",
]
