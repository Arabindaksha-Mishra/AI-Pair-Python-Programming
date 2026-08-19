# 📘 Enterprise Data Engineering Architecture & Mentor Manual
### AI Pair Python Programming — Capstone Data Quality Assistant
**Author:** Senior Python Engineering Team  
**Version:** `2.0.0` | **Specification:** PEP 621 / `uv` / Clean Code Standard  

---

## 📑 Table of Contents
1. [Executive Summary & Mentor Talking Points](#-1-executive-summary)
2. [Architectural Overview & Layout](#-2-architectural-overview)
3. [Complex Data Handling & Transformation](#-3-complex-data-handling)
   - [3.1 Type Inference & Multi-Currency](#31-type-inference)
   - [3.2 Multi-Format Date Standardization](#32-date-standardization)
   - [3.3 Comprehensive Null Token Detection](#33-null-token-detection)
   - [3.4 Order-Preserved Matrix Deduplication](#34-matrix-deduplication)
   - [3.5 Robust Statistical Imputation](#35-statistical-imputation)
   - [3.6 Statistical Outlier Capping](#36-outlier-capping)
4. [Enterprise Error Handling & Fault Resilience](#-4-error-handling)
5. [Structured Telemetry & 1-Hour Rotating Logging](#-5-logging)
6. [User Manual & Step-by-Step Execution Guide](#-6-user-manual)
   - [6.1 Interactive Terminal Launcher](#61-terminal-launcher)
   - [6.2 CLI Batch Dataset Cleaning](#62-cli-batch-cleaning)
   - [6.3 Programmatic Python API Usage](#63-python-api-usage)
7. [Verification, CI/CD Pipeline & Security](#-7-verification-and-ci)

---

## 🎯 1. Executive Summary & Mentor Talking Points

When presenting this project to your mentor or technical leads, highlight
the **3 core pillars**:

```text
┌───────────────────────────────────────────────────────────────────────┐
│                          THE 3 CORE PILLARS                           │
├───────────────────────────┬───────────────────────────┬───────────────┤
│ 1. Standard Library First │ 2. Modular Architecture   │ 3. CI/CD &    │
│ • 0 third-party runtime   │ • Separated transformer   │    Security   │
│   dependencies (No pandas)│   package from cleaner    │ • 40 Tests    │
│ • Pure Python 3.12+       │ • Single-responsibility   │ • AST Agent   │
│ • High execution speed    │   pure functions          │ • GitHub CI   │
└───────────────────────────┴───────────────────────────┴───────────────┘
```

### Key Questions Mentors Ask & Your Answers:
1. **"Why not just use Pandas or Scikit-learn?"**
   * *Answer:* Relying solely on external libraries hides algorithmic
     complexities. By implementing statistical imputation, Tukey's IQR
     fences, and type inference using Python's standard library, we
     demonstrate **deep algorithmic mastery**, zero-dependency
     deployment, and a lightweight memory footprint.
2. **"How does this pipeline handle unexpected dirty data in production?"**
   * *Answer:* The engine features **heuristic schema inference** that
     automatically detects missing tokens (`"NA"`, `"N/A"`, `"?"`, `"-"`),
     multi-locale currencies (`$1,234.50`, `(€50.00)`), and arbitrary
     date formats without crashing.
3. **"How do you ensure data integrity without loss?"**
   * *Answer:* Instead of blindly dropping rows containing extreme
     outliers, we apply **Winsorization capping** using interquartile
     fences ($Q_1 - 1.5 \cdot \text{IQR}, Q_3 + 1.5 \cdot \text{IQR}$)
     to bound values within valid statistical distributions.

---

## 🏛️ 2. Architectural Overview & Layout

The project adheres to the modern **`src/` layout** recommended by PyPA:

```text
AI-Pair-Python-Programming/
├── RN.json                  # Release Notes & Version Specification
├── pyproject.toml           # PEP 621 / uv build configuration
├── README.md                # Project documentation & quickstart
├── run_all.py               # Master interactive terminal launcher
├── test_suite.py            # Master automated test runner (40 Tests)
│
├── 🚀 CI/                   # Continuous Integration & Quality Suite
│   ├── __init__.py          # CI package metadata
│   ├── check_line_length.py # 88-column width auditor
│   ├── validate_release_notes.py # RN.json schema validator
│   └── run_quality_checks.py # Master CI pipeline runner
│
├── 📁 logs/                 # 1-Hour Time-Based Rotating Log Directory
│   └── app.log              # Active hourly log stream
│
├── 📖 docs/                 # Engineering Documentation
│   ├── CODING_STANDARDS.md  # Uncle Bob Clean Code heuristics
│   ├── TECHNICAL_DOCUMENTATION.md # Full architecture specification
│   ├── DATASET_VALIDATION_GUIDE.md # Dirty dataset validation guide
│   └── MENTOR_ANALYSIS_AND_USER_MANUAL.md # This guide
│
├── 📦 src/ai_pair_programming/ # Root Python Package
│   ├── __init__.py          # Package metadata & re-exports
│   ├── main.py              # CLI entrypoint
│   │
│   ├── 📡 telemetry/        # Structured Logging & File Rotation
│   │   ├── __init__.py      # Exports OutputHandler & get_logger
│   │   └── output_handler.py # 1-Hour Rotating Handler Engine
│   │
│   ├── 🧩 algorithms/       # Senior Domain Algorithms
│   │   ├── collections_ops.py # Unique Elements & Set Algebra
│   │   ├── numeric_math.py  # Number Theory, Fibonacci & Sequences
│   │   ├── string_utils.py  # Anagram Solvers & String NLP
│   │   └── interactive_loops.py # Interactive Sentinels & Pricing REPL
│   │
│   ├── ⚙️ data_transformer/ # Core Reusable Data Transformer Engine
│   │   ├── sanitizer.py     # Currency Parsing & Type Inference
│   │   ├── deduplicator.py  # Order-Preserved Deduplication
│   │   ├── imputer.py       # Statistical Imputation (Mean, Median, Mode)
│   │   ├── outlier_handler.py # IQR Fences & Winsorization
│   │   └── io_utils.py      # Safe CSV Ingestion & Disk Export
│   │
│   ├── 🧹 data_cleaner/      # Capstone: Tabular Cleaning Pipeline
│   │   ├── cleaner_engine.py # Pipeline Orchestrator & Profile
│   │   ├── reporter.py      # Formatted Terminal Audit Reporter
│   │   └── main.py          # Interactive & Batch CLI Runner
│   │
│   └── 🛠️ tools/             # Enterprise Developer Tools
│       ├── code_review_agent.py # AST-based Static Security Agent
│       └── version_manager.py # RN.json Release Notes Manager
│
└── 🧪 tests/                # Automated Test Suites (40 Tests Passing)
```

---

## ⚙️ 3. Complex Data Handling & Transformation Engine

The transformation engine in `data_transformer/` handles challenging
data quality anomalies:

```text
┌───────────────────────────────────────────────────────────────────────┐
│                  DATA TRANSFORMATION PIPELINE PHASES                  │
├───────────────────┬───────────────────┬───────────────┬───────────────┤
│ 1. INGEST & CAST  │ 2. DEDUPLICATION  │ 3. IMPUTATION │ 4. OUTLIERS   │
│ • Raw CSV read    │ • Order-preserved │ • Mean/Median │ • Tukey's IQR │
│ • Strip currency  │ • Full-row hash   │   numerical   │ • Winsorize   │
│ • ISO 8601 dates  │ • Column key match│ • Mode text   │ • Audit delta │
└───────────────────┴───────────────────┴───────────────┴───────────────┘
```

### 3.1 Type Inference & Multi-Currency Sanitization
* **Challenge:** Raw CSV values arrive as mixed strings:
  `"$1,250.00"`, `"-$45.50"`, `"($120.00)"`, `"€3.400,00"`.
* **Solution (`sanitizer.py`):**
  - Strips currency symbols (`$`, `€`, `£`, `¥`), commas, and whitespace.
  - Converts accounting negative format `(120.00)` to `-120.00`.
  - Infers numeric types: integers $\to$ `int`, currencies $\to$ `float`.

```python
# Example Transformations:
sanitize_currency("($1,234.50)")  # Output: -1234.5
sanitize_currency("-$50.00")  # Output: -50.0
```

### 3.2 Multi-Format Date Standardization to ISO 8601
* **Challenge:** Datasets mix date formats (`08/19/2026`, `2026-08-19`, `19-08-2026`).
* **Solution (`sanitizer.py`):**
  - Parses dates against known international format patterns.
  - Standardizes valid dates into strict **ISO 8601 (`YYYY-MM-DD`)**.

### 3.3 Comprehensive Null Token Detection
* **Challenge:** Missing values are represented as arbitrary strings:
  `"NA"`, `"N/A"`, `"null"`, `"None"`, `"missing"`, `"?"`, `"-"`, `""`.
* **Solution (`sanitizer.py`):**
  - `is_null_token(value)` maps all known representations to `None`.

### 3.4 Order-Preserved Matrix Deduplication
* **Challenge:** Standard `list(set(...))` scrambles row ordering.
* **Solution (`deduplicator.py`):**
  - Uses `dict.fromkeys()` hashing on normalized row tuples.
  - Guarantees $O(N)$ linear-time duplicate elimination while
    **strictly preserving insertion order**.

### 3.5 Robust Statistical Imputation (Mean, Median, Mode)
* **Challenge:** Datasets contain missing cells across numerical
  (price, age) and categorical (category, country) fields.
* **Solution (`imputer.py`):**
  - **Numerical:** Computes arithmetic mean or median over valid numbers,
    with safe fallbacks (0.0) if all values are null.
  - **Categorical:** Uses `collections.Counter` to compute the Mode
    (most frequent token), falling back to `"Unknown"`.

### 3.6 Statistical Outlier Capping (Tukey's IQR & Winsorization)
* **Challenge:** Extreme outliers (e.g. price error of `$999,999` for a book)
  distort downstream statistical distributions.
* **Solution (`outlier_handler.py`):**
  - Calculates First Quartile ($Q_1$) and Third Quartile ($Q_3$).
  - Determines Interquartile Range: $\text{IQR} = Q_3 - Q_1$.
  - Establishes Tukey's Fences:
    $$\text{Lower Bound} = Q_1 - 1.5 \cdot \text{IQR}$$
    $$\text{Upper Bound} = Q_3 + 1.5 \cdot \text{IQR}$$
  - Applies **Winsorization Capping**: Values exceeding bounds are capped
    to threshold limits rather than being dropped.

---

## 🛡️ 4. Enterprise Error Handling & Fault Resilience

The codebase implements defensive engineering patterns:

1. **Non-Fatal Graceful Recovery**:
   - Unrecognized date strings are safely preserved without crashing.
2. **Zero-Division & Variance Guards**:
   - Outlier handlers check for empty lists or zero variance before math.
3. **No Bare `except:` Clauses**:
   - All exceptions specify exact types (`ValueError`, `TypeError`, `OSError`)
     to prevent swallowing `KeyboardInterrupt` or `SystemExit`.
4. **No Mutable Default Arguments**:
   - Functions use `None` default arguments and initialize inside function bodies.

---

## 📡 5. Structured Telemetry & 1-Hour Rotating Logging

Logging is managed via
[`output_handler.py`](../src/ai_pair_programming/telemetry/output_handler.py):

* **📁 Centralized `logs/` Folder**: Isolated and ignored in `.gitignore`.
* **⏰ 1-Hour Time-Based Rotation**:
  `TimedRotatingFileHandler(when="h", interval=1)`
  rotates logs hourly (`app.log.YYYY-MM-DD_HH`) with a 7-day retention limit.
* **🌈 Colorized Terminal Stream**: ANSI formatting (Green=INFO, Red=ERROR).
* **📊 Step-Level Transformation Audit**:
  ```text
  2026-08-19 19:44:49 | INFO | data_cleaner : Step: Deduplication | In: 100 | Out: 95
  2026-08-19 19:44:49 | INFO | data_cleaner : Imputation filled 4 null entries.
  2026-08-19 19:44:49 | INFO | data_cleaner : Winsorization capped 1 outlier.
  ```

---

## 📖 6. User Manual & Step-by-Step Execution Guide

### 6.1 Interactive Terminal Launcher
Launch the master terminal interface:
```bash
python3 run_all.py
```
```text
==================================================================
   🚀 AI PAIR PROGRAMMING: SENIOR PYTHON SUITE & CAPSTONE
==================================================================
PART 1: Senior Python Exercises (Domain Groups)
  1.  📦 Collections & Sets       : Unique Elements (Q1), Set Ops (Q10)
  2.  🔢 Numerical Math & Series  : Perfect Numbers, Fibonacci, Squares
  3.  🔤 String Processing & NLP  : Anagram Solver, Pizza Statements
  4.  🔄 Interactive Loops & REPL : Pizza Toppings, Movie Tickets

PART 2: Capstone Project (AI-Powered Data Quality)
  5.  🧹 Automated Data Cleaning Assistant (Imputation, Outliers)

VERIFICATION, QUALITY & CI PIPELINE
  P.  Run Complete CI Pipeline (Format, Lint, 88-Col, Security, Tests)
  T.  Run Automated Test Suite (40 Tests, 100% Pass Rate)
  C.  Run Automated Security & Code Bug Review Agent
  V.  View Release Notes & Version History (RN.json)
  Q.  Quit
--------------------------------------------------------------------
```

### 6.2 CLI Batch Dataset Cleaning
Clean any CSV dataset directly from the terminal:
```bash
# Clean the built-in dirty ecommerce dataset
python3 -m ai_pair_programming.data_cleaner.main

# Or clean any arbitrary custom CSV dataset
python3 -m ai_pair_programming.data_cleaner.main /path/to/my_data.csv
```

### 6.3 Programmatic Python API Usage
Incorporate the cleaning engine into external pipelines:

```python
from ai_pair_programming.data_cleaner.cleaner_engine import (
    DataCleaningAssistant,
    DatasetProfile,
)

# 1. Define schema profile
profile = DatasetProfile(
    date_columns=["order_date"],
    currency_columns=["unit_price", "total_amount"],
    numeric_impute_strategy="median",
    categorical_impute_strategy="mode",
    enable_outlier_capping=True,
)

# 2. Initialize assistant and clean dataset
assistant = DataCleaningAssistant(profile)
cleaned_headers, cleaned_rows = assistant.clean_dataset(
    headers=["order_id", "order_date", "unit_price", "category"],
    rows=[
        ["101", "08/19/2026", "$150.00", "Electronics"],
        ["102", "2026-08-19", "NA", "Electronics"],
        ["101", "08/19/2026", "$150.00", "Electronics"],
    ],
)
```

---

## 🔒 7. Verification, CI/CD Pipeline & Security

Every modification is validated against **4 automated gates**:

```bash
# 1. Run Complete CI Quality Pipeline locally
python3 CI/run_quality_checks.py

# 2. Run Master Automated Test Suite (40 Tests)
python3 test_suite.py

# 3. Run Static AST Security & Bug Review Agent
python3 -m ai_pair_programming.tools.code_review_agent

# 4. Validate Version Management & Release Notes
python3 -m ai_pair_programming.tools.version_manager
```

### Continuous Integration (GitHub Actions)
On every commit and pull request, `.github/workflows/ci.yml` executes:
* Ruff formatting check (`ruff format --check .`)
* Ruff linter check (`ruff check .`)
* Strict 88-column width check (`python3 CI/check_line_length.py`)
* Release notes schema validation (`python3 CI/validate_release_notes.py`)
* AST security agent check (`python3 -m ai_pair_programming.tools.code_review_agent`)
* Multi-version test matrix on **Python 3.12** and **Python 3.13** (40 tests).

---

## 📊 Summary Reference Table

| Feature | Implementation | Module Path |
| :--- | :--- | :--- |
| **Type Inference** | Regex & Casting | `.../sanitizer.py` |
| **Deduplication** | Order-Preserved Set | `.../deduplicator.py` |
| **Missing Imputation** | Mean, Median, Mode | `.../imputer.py` |
| **Outlier Handling** | Tukey's IQR Bounds | `.../outlier_handler.py` |
| **Hourly Logging** | 1-Hour Rotating Log | `.../output_handler.py` |
| **Security Agent** | Custom AST Visitor | `.../code_review_agent.py` |
| **Release Tracker** | `RN.json` Manager | `.../version_manager.py` |
| **CI Automation** | Multi-Gate Verifier | `CI/run_quality_checks.py` |
