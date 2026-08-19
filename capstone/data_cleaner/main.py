"""
Interactive Terminal Entrypoint for Task 2: Data Cleaning Assistant
====================================================================
Runs the data cleaning pipeline on sample datasets or custom CSV files.
"""

import os
import sys
from capstone.data_cleaner.cleaner_engine import DataCleaningAssistant
from capstone.data_cleaner.reporter import generate_audit_report


def run_data_cleaner_cli() -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    datasets_dir = os.path.join(current_dir, "datasets")

    house_csv = os.path.join(datasets_dir, "house_prices_dirty.csv")
    ecommerce_csv = os.path.join(datasets_dir, "ecommerce_orders_dirty.csv")

    assistant = DataCleaningAssistant()

    print("\n" + "=" * 65)
    print("   🧹 Automated Data Cleaning Assistant (Standard Library)   ")
    print("=" * 65)
    print("Select a dataset to clean:")
    print("1. House Price Prediction Dataset (Dirty CSV)")
    print("2. E-Commerce Orders Dataset (Dirty CSV)")
    print("3. Custom CSV file path")
    print("4. Exit")

    choice = input("\nEnter choice [1-4]: ").strip()

    if choice == "1":
        target_file = house_csv
        name = "House Prices"
    elif choice == "2":
        target_file = ecommerce_csv
        name = "E-Commerce Orders"
    elif choice == "3":
        target_file = input("Enter path to your CSV file: ").strip()
        name = os.path.basename(target_file)
        if not os.path.isfile(target_file):
            print(f"Error: File '{target_file}' does not exist.")
            return
    else:
        print("Exiting.")
        return

    print(f"\nProcessing '{name}' from: {target_file} ...")
    headers, raw_rows = assistant.load_csv(target_file)

    profile = assistant.clean_dataset(headers, raw_rows)
    report_text = generate_audit_report(profile, dataset_name=name)
    print(report_text)

    # Option to export cleaned CSV
    export_choice = input("Would you like to export the cleaned CSV? (y/n): ").strip().lower()
    if export_choice in ("y", "yes"):
        out_path = target_file.replace(".csv", "_cleaned.csv")
        assistant.save_csv(out_path, profile.headers, profile.rows)
        print(f"✅ Cleaned dataset successfully exported to: {out_path}")


if __name__ == "__main__":
    run_data_cleaner_cli()
