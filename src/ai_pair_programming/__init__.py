"""
AI Pair Python Programming Package
==================================
Standard library engineering suite organized into functional domain groups:
- exercises   : Task 1 Senior Exercises (Collections, Math, Strings, Loops)
- capstone    : Task 2 AI-Powered Tabular Data Cleaning Assistant
- constants   : Global Magic Numbers, RegEx Patterns, Defaults & Null Tokens
- exceptions  : Domain Exception Hierarchy (AIPairProgrammingError, etc.)
- models      : Data Models (TabularDataset, CleaningConfig, Type Aliases)
- telemetry   : Structured Logging and 1-hour Rotating File Handlers
- tools       : AST Security Reviewer and Version Management Utilities
"""

from __future__ import annotations

from .constants import (
    DEFAULT_IQR_FACTOR,
    DEFAULT_Z_SCORE_THRESHOLD,
    NULL_STRINGS,
    SUPPORTED_DATE_FORMATS,
)
from .exceptions import (
    AIPairProgrammingError,
    ColumnNotFoundError,
    DataCleanerError,
    DatasetValidationError,
    FileProcessingError,
    ReleaseNotesSchemaError,
    VersionManagerError,
)
from .models import (
    CastResult,
    CleaningConfig,
    PrimitiveValue,
    RawCellValue,
    ReleaseRecord,
    TabularDataset,
    TabularMatrix,
    TabularRow,
)
from .telemetry.output_handler import (
    OutputHandler,
    get_logger,
    get_logs_directory,
)

__version__ = "2.0.0"
__all__ = [
    "DEFAULT_IQR_FACTOR",
    "DEFAULT_Z_SCORE_THRESHOLD",
    "NULL_STRINGS",
    "SUPPORTED_DATE_FORMATS",
    "AIPairProgrammingError",
    "CastResult",
    "CleaningConfig",
    "ColumnNotFoundError",
    "DataCleanerError",
    "DatasetValidationError",
    "FileProcessingError",
    "OutputHandler",
    "PrimitiveValue",
    "RawCellValue",
    "ReleaseNotesSchemaError",
    "ReleaseRecord",
    "TabularDataset",
    "TabularMatrix",
    "TabularRow",
    "VersionManagerError",
    "__version__",
    "get_logger",
    "get_logs_directory",
]
