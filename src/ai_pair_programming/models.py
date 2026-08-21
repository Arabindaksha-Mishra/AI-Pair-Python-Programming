"""
Capstone & System Data Models & Explicit Type Aliases
======================================================
Provides strongly-typed domain aliases and memory-optimized dataclass models:
- Type Aliases : PrimitiveValue, RawCellValue, CastResult, TabularRow, TabularMatrix
- Data Models  : TabularDataset, CleaningConfig, ReleaseRecord

100% Pure Standard Library (PEP 681 Dataclasses with slots=True).
"""

from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any

PrimitiveValue = str | int | float | bool | None
RawCellValue = object
CastResult = tuple[PrimitiveValue, str]
TabularRow = list[PrimitiveValue]
TabularMatrix = list[TabularRow]


@dataclass(slots=True)
class TabularDataset:
    """
    Strongly-typed representation of a tabular dataset with headers and 2D matrix.
    """

    headers: list[str]
    rows: TabularMatrix
    dataset_name: str = "Dataset"

    @property
    def num_rows(self) -> int:
        """Return total row count in matrix."""
        return len(self.rows)

    @property
    def num_cols(self) -> int:
        """Return total column count from headers."""
        return len(self.headers)

    @property
    def shape(self) -> tuple[int, int]:
        """Return (num_rows, num_cols) tuple."""
        return (self.num_rows, self.num_cols)


@dataclass(slots=True)
class CleaningConfig:
    """
    Configuration parameters for DataCleaningAssistant pipeline execution.
    """

    iqr_factor: float = 1.5
    z_score_threshold: float = 3.0
    numeric_impute_strategy: str = "median"
    categorical_impute_strategy: str = "mode"


@dataclass(slots=True)
class ReleaseRecord:
    """
    Data model representing a version change item in release_notes.json.
    """

    version: float
    component: str
    description: str
    category: str
    epoch_timestamp: int = field(default_factory=lambda: int(time.time()))
    is_new: bool = True
    is_deleted: bool = False
    is_breaking: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert dataclass instance to JSON-serializable dictionary."""
        return {
            "category": self.category,
            "component": self.component,
            "description": self.description,
            "epoch_timestamp": self.epoch_timestamp,
            "is_breaking": self.is_breaking,
            "is_deleted": self.is_deleted,
            "is_new": self.is_new,
            "version": self.version,
        }
