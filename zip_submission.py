"""
Submission Zip Packager
=======================
Automates creating a clean, lightweight zip archive for trainer submission,
excluding bytecode cache, git history, and temporary files.

Usage:
    python3 zip_submission.py
"""

import os
import zipfile

EXCLUDE_DIRS = {"__pycache__", ".git", ".pytest_cache", ".vscode", ".idea"}
EXCLUDE_EXTS = {".pyc", ".pyo", ".pyd", ".zip"}


def create_submission_zip(output_zip: str = "ai_pair_programming_capstone_submission.zip") -> str:
    root_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(root_dir, output_zip)

    if os.path.exists(zip_path):
        os.remove(zip_path)

    file_count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(root_dir):
            # Prune excluded directories in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in EXCLUDE_EXTS or file.startswith("."):
                    continue

                abs_file = os.path.join(root, file)
                rel_path = os.path.relpath(abs_file, root_dir)

                zipf.write(abs_file, arcname=os.path.join("ai_pair_programming_capstone", rel_path))
                file_count += 1

    file_size_kb = os.path.getsize(zip_path) / 1024
    print(f"✅ Created submission archive: {output_zip}")
    print(f"📦 Files packaged: {file_count}")
    print(f"📏 Archive size:   {file_size_kb:.2f} KB")
    return zip_path


if __name__ == "__main__":
    create_submission_zip()
