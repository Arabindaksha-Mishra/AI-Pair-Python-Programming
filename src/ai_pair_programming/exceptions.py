"""
Domain Specific Exceptions Hierarchy
=====================================
Defines structured, custom exception classes for robust error handling across:
- Capstone Data Cleaning Assistant (DatasetValidationError, FileProcessingError)
- Release & Versioning Tools (VersionManagerError, ReleaseNotesSchemaError)

100% Pure Standard Library.
"""

from __future__ import annotations


class AIPairProgrammingError(Exception):
    """Base exception class for all custom project errors."""

    pass


class DataCleanerError(AIPairProgrammingError):
    """Base exception for Capstone Data Cleaning Assistant pipeline errors."""

    pass


class DatasetValidationError(DataCleanerError):
    """Raised when an input tabular dataset or matrix is empty or invalid."""

    pass


class ColumnNotFoundError(DataCleanerError):
    """Raised when accessing a column header or index that does not exist."""

    pass


class FileProcessingError(DataCleanerError):
    """Raised when CSV reading or writing operations fail."""

    pass


class VersionManagerError(AIPairProgrammingError):
    """Base exception for Version Manager and Release Notes tools."""

    pass


class ReleaseNotesSchemaError(VersionManagerError):
    """Raised when release_notes.json fails validation or schema checks."""

    pass
