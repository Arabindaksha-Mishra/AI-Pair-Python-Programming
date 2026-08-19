# 🚀 AI Pair Python Programming — Senior Capstone Suite

An enterprise-grade Python 3.12+ repository built with modern `uv` / `src`-layout
standards, zero external runtime dependencies, comprehensive test automation,
centralized hourly rotating logging, and `RN.json` release notes management.

---

## ⚡ Quick Start

### 1. Launch Master Interactive Menu
```bash
python3 run_all.py
```
*(Opens interactive launcher for domain algorithms, cleaner, and tools)*

### 2. View Release Notes & Version History (RN.json)
```bash
python3 -m ai_pair_programming.tools.version_manager
```

### 3. Run Automated Security & Code Bug Review Agent
```bash
python3 -m ai_pair_programming.tools.code_review_agent
```
*(Performs static AST inspection for security flaws and defect patterns)*

### 4. Run All Automated Tests (40 Tests)
```bash
python3 test_suite.py
# or
python3 -m unittest discover tests
```
*(Executes all 40 unit and integration tests with 100% pass rate)*

---

## 📂 Modern `uv` & `src/` Architecture

```text
AI-Pair-Python-Programming/
├── RN.json                      # 📋 Release Notes & Version Specification
├── pyproject.toml               # PEP 621 / uv package configuration
├── README.md                    # Quickstart guide & documentation
├── requirements.txt             # Standard runtime requirements (0 deps)
├── run_all.py                   # Master interactive launcher
├── test_suite.py                # Master automated test runner
│
├── 📁 logs/                     # 1-Hour Rotating Log Storage
│   └── app.log                  # Active hourly rotated application log
│
├── 🚀 CI/                       # Automated CI & Quality Scripts
│   ├── check_line_length.py     # 88-column limit validator
│   ├── validate_release_notes.py # RN.json schema validator
│   └── run_quality_checks.py    # Master CI pipeline runner
│
├── 📖 docs/                     # Documentation & Standards
│   ├── CODING_STANDARDS.md      # Clean Code & Readability standards
│   ├── TECHNICAL_DOCUMENTATION.md # Full engineering specification
│   └── DATASET_VALIDATION_GUIDE.md # Dirty dataset validation guide
│
├── 📦 src/
│   └── ai_pair_programming/     # Top-Level Python Package
│       ├── __init__.py          # Package metadata & re-exports
│       ├── main.py              # CLI entrypoint
│       │
│       ├── 📡 telemetry/        # Structured Logging & File Rotation
│       │   ├── __init__.py          # Re-exports OutputHandler & get_logger
│       │   └── output_handler.py    # 1-Hour Rotating Handler Engine
│       ├── 🧩 algorithms/       # Senior Domain Algorithms
│       │   ├── collections_ops.py   # Group 1: Unique & Sets
│       │   ├── numeric_math.py      # Group 2: Math & Series
│       │   ├── string_utils.py      # Group 3: Strings & NLP
│       │   └── interactive_loops.py # Group 4: Loops & Sentinels
│       │
│       ├── ⚙️ data_transformer/ # Reusable Transformation Package
│       │   ├── sanitizer.py         # Currency & Type Casting
│       │   ├── deduplicator.py      # List & Table Deduplication
│       │   ├── imputer.py           # Statistical Imputation
│       │   ├── outlier_handler.py   # IQR Fences & Winsorization
│       │   └── io_utils.py          # Safe CSV File I/O
│       │
│       ├── 🧹 data_cleaner/     # Capstone Data Cleaning Assistant
│       │   ├── cleaner_engine.py    # Pipeline Orchestrator
│       │   ├── reporter.py          # Terminal & Markdown Reporter
│       │   ├── main.py              # Interactive Cleaner CLI
│       │   └── datasets/            # Sample Dirty CSVs
│       │
│       └── 🛠️ tools/            # Security & Versioning Tools
│           ├── code_review_agent.py # AST Security Analyzer
│           └── version_manager.py   # Release Notes & Version Manager
│
└── 🧪 tests/                    # Modular Test Suites (40 Tests)
    ├── test_algorithms.py       # Domain Group Tests
    ├── test_data_transformer.py # Transformer Unit Tests
    ├── test_data_cleaner.py     # Cleaner Assistant Tests
    ├── test_output_handler.py   # Logging & Telemetry Tests
    ├── test_code_review_agent.py # AST Security Agent Tests
    ├── test_version_manager.py  # RN.json Version Tests
    └── test_e2e.py              # E2E Pipeline Integration Tests
```

---

## 📋 Release Notes & Version Management (`RN.json`)

The project uses [`RN.json`][rn-file] to track version transitions
(`1.0.0` $\to$ `1.1.0` $\to$ `2.0.0`), timestamps, categorized changes, and
validation metrics:

[rn-file]: file:///usr/local/google/home/arabindaksha/AI-Pair-Python-Programming/RN.json

```bash
# View human-readable formatted release history
python3 -m ai_pair_programming.tools.version_manager

# View raw JSON specification
python3 -m ai_pair_programming.tools.version_manager --json
```

---

## 📢 Output & Hourly Rotating Logging Engine

The `output_handler.py` module provides enterprise telemetry and log storage:

* **📁 Dedicated `logs/` Directory**: Centralizes time-stamped log files.
* **⏰ 1-Hour Time-Based Rotation**: Automates hourly log file rotation
  (`app.log.YYYY-MM-DD_HH`) via `TimedRotatingFileHandler` (retains 7 days).
* **🌈 Colorized Console Streams**: Level-specific ANSI colors (DEBUG $\to$ CRITICAL).
* **📊 Transformation Audit Logs**: Tracks step-level input, output, and delta records.

---

## 🧹 Capstone: AI-Powered Data Cleaning Assistant

The data quality pipeline is located in `src/ai_pair_programming/data_cleaner/`:

```bash
# Run interactive cleaner
python3 -m ai_pair_programming.data_cleaner.main

# Or clean any custom dataset directly
python3 -m ai_pair_programming.data_cleaner.main /path/to/custom_data.csv
```

---

## 🧪 Verification & Automated Testing

```bash
# Master runner (All 40 tests passing)
python3 test_suite.py

# Format and lint with Ruff
ruff check .
ruff format .
```
