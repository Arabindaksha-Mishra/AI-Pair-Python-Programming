"""
Data Transformer: Value Sanitizer & Type Inference Engine
==========================================================
Provides modular functions for string sanitization, currency parsing,
ISO date normalization, null token detection, and automated type casting.
"""

from __future__ import annotations

import datetime
import re
from typing import Any

from ai_pair_programming.output_handler import get_logger

_LOGGER = get_logger("data_transformer.sanitizer")

NULL_STRINGS: frozenset[str] = frozenset(
    {"", "n/a", "na", "null", "none", "nan", "-999", "?", "nil", "undefined"}
)


def is_null_token(val: Any) -> bool:
    """
    Check if a given raw value represents a missing or null value.

    Args:
        val (Any): Target value to inspect.

    Returns:
        bool: True if val is None or matches known null string tokens.

    """
    if val is None:
        return True
    return str(val).strip().lower() in NULL_STRINGS


def sanitize_text(val: str) -> str:
    """
    Strip outer whitespace and collapse internal consecutive whitespace.

    Args:
        val (str): Raw string to sanitize.

    Returns:
        str: Cleaned normalized string.

    """
    return re.sub(r"\s+", " ", val.strip())


def _extract_currency_sign_and_body(val: str) -> tuple[bool, str]:
    """
    Extract negative indicator from currency strings.

    Args:
        val (str): Raw currency string.

    Returns:
        tuple[bool, str]: (is_negative, trimmed_numeric_body).

    """
    clean = val.strip()
    if clean.startswith("(") and clean.endswith(")"):
        return True, clean[1:-1].strip()
    if clean.startswith("-"):
        return True, clean[1:].strip()
    return False, clean


def sanitize_currency(val: str) -> float | int | None:
    """
    Parse currency strings into numeric integers or floats.

    Args:
        val (str): Currency string (e.g. '$1,200.50', '($150.00)').

    Returns:
        float | int | None: Parsed numeric amount or None if parsing fails.

    """
    clean = val.strip()
    if not clean:
        return None

    is_negative, body = _extract_currency_sign_and_body(clean)
    cleaned_num = re.sub(r"[\$,€,£,¥]", "", body).replace(",", "").strip()

    try:
        if "." in cleaned_num:
            parsed_float = float(cleaned_num)
            return -parsed_float if is_negative else parsed_float
        parsed_int = int(cleaned_num)
        return -parsed_int if is_negative else parsed_int
    except ValueError:
        return None


def normalize_date(val: str) -> str | None:
    """
    Parse common date representations into ISO 'YYYY-MM-DD' format.

    Args:
        val (str): Date string in any common format.

    Returns:
        str | None: Standardized ISO date string or None if unparseable.

    """
    val_clean = val.strip()
    formats = (
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%m-%d-%Y",
        "%m/%d/%Y",
        "%Y.%m.%d",
    )
    for fmt in formats:
        try:
            parsed = datetime.datetime.strptime(val_clean, fmt)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def _try_parse_currency(s: str) -> tuple[Any, str] | None:
    """
    Attempt to parse string as currency or financial number.

    Args:
        s (str): String representation.

    Returns:
        tuple[Any, str] | None: (parsed_value, type_name) if matched.

    """
    if re.search(r"[\$,€,£,¥]", s) or re.match(r"^\(?-?[\d,]+(\.\d+)?\)?$", s):
        parsed = sanitize_currency(s)
        if parsed is not None:
            return parsed, "float" if isinstance(parsed, float) else "int"
    return None


def _try_parse_date(s: str) -> tuple[Any, str] | None:
    """
    Attempt to parse string as standardized ISO date.

    Args:
        s (str): String representation.

    Returns:
        tuple[Any, str] | None: (iso_date_string, 'date') if matched.

    """
    if re.match(r"^\d{2,4}[-/\.]\d{1,2}[-/\.]\d{1,4}$", s):
        normalized = normalize_date(s)
        if normalized is not None:
            return normalized, "date"
    return None


def _try_parse_boolean(s: str) -> tuple[Any, str] | None:
    """
    Attempt to parse boolean token.

    Args:
        s (str): String representation.

    Returns:
        tuple[Any, str] | None: (bool_value, 'bool') if matched.

    """
    lower = s.lower()
    if lower in ("true", "yes", "y", "1"):
        return True, "bool"
    if lower in ("false", "no", "n", "0"):
        return False, "bool"
    return None


def _try_parse_numeric(s: str) -> tuple[Any, str] | None:
    """
    Attempt to cast string into float or integer.

    Args:
        s (str): String representation.

    Returns:
        tuple[Any, str] | None: (numeric_value, 'float' | 'int') if matched.

    """
    try:
        if "." in s:
            return float(s), "float"
        return int(s), "int"
    except ValueError:
        return None


def infer_and_cast_value(val: Any) -> tuple[Any, str]:
    """
    Infer the native data type and cast raw value accordingly.

    Args:
        val (Any): Raw value to inspect and cast.

    Returns:
        tuple[Any, str]: (casted_value, inferred_type_name).

    """
    if is_null_token(val):
        return None, "null"

    if isinstance(val, (int, float, bool)):
        return val, type(val).__name__

    s = str(val).strip()

    currency_result = _try_parse_currency(s)
    if currency_result is not None:
        return currency_result

    date_result = _try_parse_date(s)
    if date_result is not None:
        return date_result

    bool_result = _try_parse_boolean(s)
    if bool_result is not None:
        return bool_result

    numeric_result = _try_parse_numeric(s)
    if numeric_result is not None:
        return numeric_result

    return s, "str"
