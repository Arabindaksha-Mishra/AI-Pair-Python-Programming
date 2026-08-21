"""
Release Notes & Version Management Engine
==========================================
Manages structured release tracking, version bumping, and changelog history
via the centralized `release_notes.json` metadata specification.
"""

from __future__ import annotations

import datetime
import json
import os
import sys
from typing import Any

from ai_pair_programming.telemetry import OutputHandler, get_logger


def _find_project_root() -> str:
    """
    Calculate the project root absolute filesystem path from module location.

    Returns:
        str: Absolute filesystem path to root directory.

    """
    return os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )


class VersionManager:
    """Manages project versioning, release notes, and changelog history."""

    def __init__(
        self,
        rn_file_path: str | None = None,
        logger: OutputHandler | None = None,
    ) -> None:
        """
        Initialize the VersionManager with target release_notes.json file.

        Args:
            rn_file_path (str | None): Optional path to release_notes.json file.
            logger (OutputHandler | None): Logger instance.

        Returns:
            None

        """
        if rn_file_path is None:
            project_root = _find_project_root()
            self.rn_file_path = os.path.join(project_root, "release_notes.json")
        else:
            self.rn_file_path = os.path.abspath(rn_file_path)

        self.logger = logger or get_logger("version_manager")
        self.records: list[dict[str, Any]] = self._load_records()

    def _load_records(self) -> list[dict[str, Any]]:
        """
        Load records from release_notes.json or return empty default list.

        Returns:
            list[dict[str, Any]]: List of release note change records.

        """
        if not os.path.exists(self.rn_file_path):
            self.logger.warning(
                f"release_notes.json not found at {self.rn_file_path}. "
                "Initializing default."
            )
            return []

        try:
            with open(self.rn_file_path, encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return []
        except Exception as e:
            self.logger.error(f"Failed to read release_notes.json: {e}")
            return []

    def save(self) -> None:
        """
        Persist current records list to release_notes.json on disk.

        Returns:
            None

        """
        with open(self.rn_file_path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2)
            f.write("\n")
        self.logger.info(f"Updated release notes saved to: {self.rn_file_path}")

    def get_current_version(self) -> float:
        """
        Retrieve highest active project version number.

        Returns:
            float: Highest version recorded (e.g. 2.0).

        """
        if not self.records:
            return 1.0
        versions = [float(r.get("version", 1.0)) for r in self.records]
        return max(versions)

    def get_records(self) -> list[dict[str, Any]]:
        """
        Retrieve complete list of release note records.

        Returns:
            list[dict[str, Any]]: List of release note dictionaries.

        """
        return list(self.records)

    def add_change_record(
        self,
        component: str,
        description: str,
        category: str = "Module",
        version: float = 2.0,
        is_new: bool = True,
        is_breaking: bool = False,
        is_deleted: bool = False,
        epoch_timestamp: int | None = None,
    ) -> dict[str, Any]:
        """
        Record a new release notes item in RN.json.

        Args:
            component (str): Name of the component modified.
            description (str): Details of changes applied.
            category (str): Category type (e.g. 'Module', 'Tool').
            version (float): Version number tag.
            is_new (bool): Whether component is a new addition.
            is_breaking (bool): Whether change is breaking.
            is_deleted (bool): Whether component was removed.
            epoch_timestamp (int | None): Epoch timestamp (seconds).

        Returns:
            dict[str, Any]: Created release note dictionary.

        """
        if epoch_timestamp is None:
            epoch_timestamp = int(datetime.datetime.now(datetime.UTC).timestamp())

        new_record = {
            "category": category,
            "component": component,
            "description": description,
            "epoch_timestamp": epoch_timestamp,
            "is_breaking": is_breaking,
            "is_deleted": is_deleted,
            "is_new": is_new,
            "version": float(version),
        }

        self.records.append(new_record)
        self.save()
        self.logger.info(f"Recorded change for {component} (v{version:.1f})")
        return new_record

    def format_history(self) -> str:
        """
        Format release note records into a readable terminal overview.

        Returns:
            str: Multi-line terminal summary string.

        """
        lines = [
            "\n==================================================================",
            "   📋 PROJECT RELEASE NOTES & VERSION MANAGEMENT (RN.json)",
            "==================================================================",
            f"• Current Version:  {self.get_current_version():.1f}",
            f"• Total Records:    {len(self.records)}",
            "------------------------------------------------------------------",
        ]

        version_groups: dict[float, list[dict[str, Any]]] = {}
        for r in self.records:
            v = float(r.get("version", 1.0))
            version_groups.setdefault(v, []).append(r)

        for ver in sorted(version_groups.keys(), reverse=True):
            items = version_groups[ver]
            lines.append(f"\n🚀 Version {ver:.1f} ({len(items)} changes):")
            for rec in items:
                status_tags: list[str] = []
                if rec.get("is_new"):
                    status_tags.append("NEW")
                if rec.get("is_breaking"):
                    status_tags.append("BREAKING")
                if rec.get("is_deleted"):
                    status_tags.append("REMOVED")
                tag_str = f" [{', '.join(status_tags)}]" if status_tags else ""

                component = rec.get("component", "Unknown")
                category = rec.get("category", "Item")
                desc = rec.get("description", "")
                lines.append(f"   • [{category}] {component}{tag_str}")
                lines.append(f"     Details: {desc}")

        lines.append(
            "\n==================================================================\n"
        )
        return "\n".join(lines)


def main() -> None:
    """
    Launch CLI interface for version management inspection.

    Returns:
        None

    """
    vm = VersionManager()
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        print(json.dumps(vm.records, indent=2))
        return

    print(vm.format_history())


if __name__ == "__main__":
    main()
