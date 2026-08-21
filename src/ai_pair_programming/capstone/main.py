"""
Interactive Terminal Entrypoint for Task 2: Data Cleaning Assistant
====================================================================
Runs the data cleaning pipeline on sample datasets or custom CSV files.
"""

from __future__ import annotations

import os
import sys

from ai_pair_programming.telemetry import get_logger

from .cleaner_engine import DataCleaningAssistant, DatasetProfile
from .reporter import generate_audit_report

_LOGGER = get_logger("data_cleaner.cli")


def _process_dataset(
    assistant: DataCleaningAssistant, target_file: str, name: str
) -> DatasetProfile:
    """
    Load, clean, and print audit report for a target dataset.

    Args:
        assistant (DataCleaningAssistant): Cleaning engine instance.
        target_file (str): Filesystem path to target CSV.
        name (str): Label identifying the dataset.

    Returns:
        DatasetProfile: Generated profile containing cleaned dataset.

    """
    _LOGGER.info(f"Processing dataset '{name}' from path: {target_file}")
    print(f"\nProcessing '{name}' from: {target_file} ...")
    headers, raw_rows = assistant.load_csv(target_file)
    profile = assistant.clean_dataset(headers, raw_rows)
    report_text = generate_audit_report(profile, dataset_name=name)
    print(report_text)
    return profile


def _prompt_export_cleaned(
    assistant: DataCleaningAssistant,
    target_file: str,
    profile: DatasetProfile,
) -> None:
    """
    Prompt user via terminal to export cleaned dataset to disk.

    Args:
        assistant (DataCleaningAssistant): Cleaning engine instance.
        target_file (str): Original dataset path.
        profile (DatasetProfile): Cleaned dataset profile.

    Returns:
        None

    """
    try:
        export_choice = (
            input("Would you like to export the cleaned CSV? (y/n): ").strip().lower()
        )
    except (KeyboardInterrupt, EOFError):
        return

    if export_choice in ("y", "yes"):
        out_path = os.path.splitext(target_file)[0] + "_cleaned.csv"
        assistant.save_csv(out_path, profile.headers, profile.rows)
        _LOGGER.info(f"Exported cleaned CSV to: {out_path}")
        print(f"✅ Cleaned dataset successfully exported to: {out_path}\n")


def _select_dataset(house_csv: str, ecommerce_csv: str) -> tuple[str, str] | None:
    """
    Render interactive CLI menu for dataset selection.

    Args:
        house_csv (str): Path to house prices sample dataset.
        ecommerce_csv (str): Path to e-commerce sample dataset.

    Returns:
        tuple[str, str] | None: (dataset_path, display_name) or None if
            cancelled or exiting.

    """
    print("\n" + "=" * 65)
    print("   🧹 Automated Data Cleaning Assistant (Standard Library)   ")
    print("=" * 65)
    print("Select a dataset to clean:")
    print("1. House Price Prediction Dataset (Dirty CSV)")
    print("2. E-Commerce Orders Dataset (Dirty CSV)")
    print("3. Custom CSV file path")
    print("4. Exit")

    try:
        choice = input("\nEnter choice [1-4]: ").strip()
    except (KeyboardInterrupt, EOFError):
        return None

    if choice == "1":
        return house_csv, "House Prices"
    if choice == "2":
        return ecommerce_csv, "E-Commerce Orders"
    if choice == "3":
        try:
            custom_path = input("Enter path to your CSV file: ").strip()
        except (KeyboardInterrupt, EOFError):
            return None
        if not os.path.isfile(custom_path):
            _LOGGER.error(f"Provided file does not exist: {custom_path}")
            print(f"Error: File '{custom_path}' does not exist.")
            return None
        return custom_path, os.path.basename(custom_path)
    return None


def run_data_cleaner_cli() -> None:
    """
    Launch master CLI interface for data cleaning assistant.

    Returns:
        None

    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    datasets_dir = os.path.join(current_dir, "datasets")
    house_csv = os.path.join(datasets_dir, "house_prices_dirty.csv")
    ecommerce_csv = os.path.join(datasets_dir, "ecommerce_orders_dirty.csv")

    assistant = DataCleaningAssistant()

    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        target_file = sys.argv[1]
        name = os.path.basename(target_file)
        if not os.path.isfile(target_file):
            _LOGGER.error(f"Command line target file not found: {target_file}")
            print(f"Error: File '{target_file}' does not exist.")
            sys.exit(1)
        profile = _process_dataset(assistant, target_file, name)
        out_path = os.path.splitext(target_file)[0] + "_cleaned.csv"
        assistant.save_csv(out_path, profile.headers, profile.rows)
        print(f"✅ Cleaned dataset successfully exported to: {out_path}\n")
        return

    selection = _select_dataset(house_csv, ecommerce_csv)
    if selection is None:
        return

    target_file, name = selection
    profile = _process_dataset(assistant, target_file, name)
    _prompt_export_cleaned(assistant, target_file, profile)


if __name__ == "__main__":
    run_data_cleaner_cli()
