"""
Telemetry Subsystem
===================
Provides structured logging, colorized console streams, and 1-hour interval
rotating file handlers.
"""

from __future__ import annotations

from .output_handler import (
    ColorLogFormatter,
    OutputHandler,
    get_logger,
    get_logs_directory,
)

__all__ = [
    "ColorLogFormatter",
    "OutputHandler",
    "get_logger",
    "get_logs_directory",
]
