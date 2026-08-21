"""
CI Utility: Release Notes Specification Validator
=================================================
Validates presence, syntax, schema conformity, and integrity of release_notes.json.
"""

from __future__ import annotations

import json
import os
import sys

REQUIRED_FIELDS: set[str] = {
    "category",
    "component",
    "description",
    "epoch_timestamp",
    "is_breaking",
    "is_deleted",
    "is_new",
    "version",
}


def validate_rn_file(file_path: str = "release_notes.json") -> list[str]:
    """
    Validate the format and required fields of target release_notes.json file.

    Args:
        file_path (str): Path to release notes JSON file.

    Returns:
        list[str]: List of error strings, or empty list if valid.

    """
    errors: list[str] = []

    if not os.path.isfile(file_path):
        return [f"Release notes file not found: {file_path}"]

    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [f"Failed to parse JSON in {file_path}: {e}"]

    if not isinstance(data, list):
        return [f"Root of {file_path} must be a list of change records."]

    if not data:
        return [f"{file_path} contains zero change records."]

    for idx, record in enumerate(data, 1):
        if not isinstance(record, dict):
            errors.append(f"Record #{idx} is not a valid JSON dictionary.")
            continue

        record_keys = set(record.keys())
        missing = REQUIRED_FIELDS - record_keys
        if missing:
            errors.append(
                f"Record #{idx} ('{record.get('component', 'Unknown')}') "
                f"missing required fields: {sorted(missing)}"
            )

        if not isinstance(record.get("version"), (int, float)):
            errors.append(f"Record #{idx} 'version' must be numeric (int/float).")

        if not isinstance(record.get("epoch_timestamp"), int):
            errors.append(f"Record #{idx} 'epoch_timestamp' must be integer timestamp.")

    return errors


def main() -> None:
    """
    CLI entrypoint for release_notes.json validation in CI pipeline.

    Returns:
        None

    """
    path = sys.argv[1] if len(sys.argv) > 1 else "release_notes.json"
    errors = validate_rn_file(path)

    if errors:
        print(f"❌ release_notes.json Validation Failed: Found {len(errors)} issues:")
        for err in errors:
            print(f"  • {err}")
        sys.exit(1)

    print("✅ release_notes.json specification validated successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
