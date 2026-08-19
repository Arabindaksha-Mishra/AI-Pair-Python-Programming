# AI Pair Python Programming — Technical Documentation & Architecture

> **Submission Package:** `ai_pair_programming_capstone_submission.zip`  
> **Packaging Standard:** Modern `uv` / PEP 621 / `src`-Layout  
> **Environment:** Python 3.12+ (Linux / macOS / Windows)  
> **External Dependencies:** **NONE (100% Python Standard Library)**  
> **API Keys Required:** **NONE (100% Offline & Deterministic)**  

---

## 1. Executive Summary & Design Principles

This repository delivers an enterprise-grade solution for the **AI Pair
Python Programming** curriculum, structured using modern packaging best
practices:
1. **`src`-Layout Packaging:** All business logic, algorithms, and engines
   reside cleanly inside `src/ai_pair_programming/`.
2. **Functional Domain Grouping:**
   - `algorithms/`: Discrete mathematical, linguistic, and loop algorithms.
   - `data_transformer/`: Reusable sanitizers, deduplicators, imputers.
   - `data_cleaner/`: Production tabular data cleaning engine.
   - `output_handler.py`: Centralized structured logging and telemetry.
   - `tools/`: AST-based security auditing agent and RN.json version manager.
3. **Quality & Verification:** 100% automated test coverage across `tests/`.

---

## 2. Repository & Package Architecture

```text
AI-Pair-Python-Programming/
├── RN.json                      # Release Notes & Version Specification
├── pyproject.toml               # PEP 621 / uv package configuration
├── README.md                    # Quickstart guide & documentation
├── requirements.txt             # Standard runtime requirements (0 deps)
├── run_all.py                   # Master interactive terminal launcher
├── test_suite.py                # Master automated test suite runner
│
├── logs/                        # 1-Hour Rotating Log Storage
│   └── app.log                  # Active hourly rotated application log
│
├── ci/                          # Automated CI & Quality Tools
│   ├── check_line_length.py     # 88-column limit validator
│   ├── validate_release_notes.py # RN.json schema validator
│   └── run_quality_checks.py    # Master CI pipeline runner
│
├── docs/                        # Project Documentation
│   ├── CODING_STANDARDS.md      # Clean Code & Readability standards
│   ├── TECHNICAL_DOCUMENTATION.md # Full architectural specification
│   └── DATASET_VALIDATION_GUIDE.md # Test dataset validation spec
│
├── src/                         # Source Code (uv / PEP 517 standard)
│   └── ai_pair_programming/     # Top-Level Namespace
│       ├── __init__.py          # Re-exports and version metadata
│       ├── main.py              # CLI entrypoint
│       │
│       ├── telemetry/           # Structured Logging & File Rotation
│       │   ├── __init__.py          # Re-exports OutputHandler & get_logger
│       │   └── output_handler.py    # 1-Hour Rotating Handler Engine
│       ├── algorithms/          # Functional Group: Part 1 Exercises
│       │   ├── collections_ops.py   # Q1 (Unique) & Q10 (Set ops)
│       │   ├── numeric_math.py      # Q2, Q3, Q6, Q8 Math Algorithms
│       │   ├── string_utils.py      # Q7 (Pizza), Q9 (Anagram solver)
│       │   └── interactive_loops.py # Q4 (Sentinel), Q5 (Pricing)
│       │
│       ├── data_transformer/   # Reusable Transformation Engine
│       │   ├── sanitizer.py         # Currency & Type Casting
│       │   ├── deduplicator.py      # Order-preserved Deduplication
│       │   ├── imputer.py           # Statistical Imputation
│       │   ├── outlier_handler.py   # IQR Fences & Winsorization
│       │   └── io_utils.py          # Safe CSV File I/O
│       │
│       ├── data_cleaner/        # Functional Group: Part 2 Capstone
│       │   ├── cleaner_engine.py    # Imputation, Outliers, Types
│       │   ├── reporter.py          # Audit Report Generator
│       │   ├── main.py              # Data Cleaner CLI Entrypoint
│       │   └── datasets/            # Dirty CSV Sample Datasets
│       │
│       └── tools/               # Functional Group: Tools & Security
│           ├── code_review_agent.py # AST-based Static Security Agent
│           └── version_manager.py   # Release Notes & Version Manager
│
└── tests/                       # Modular Test Suites (40 Tests)
    ├── test_algorithms.py       # Domain Group Tests
    ├── test_data_transformer.py # Transformer Unit Tests
    ├── test_data_cleaner.py     # Cleaner Assistant Tests
    ├── test_output_handler.py   # Logging & Telemetry Tests
    ├── test_code_review_agent.py # AST Security Agent Tests
    ├── test_version_manager.py  # RN.json Version Tests
    └── test_e2e.py              # E2E Pipeline Integration Tests
```

---

## 3. Verification & Code Review Guide

### 1. Run Master Test Suite
```bash
python3 test_suite.py
```

### 2. Run Static Security & Code Bug Review Agent
```bash
python3 -m ai_pair_programming.tools.code_review_agent
```

### 3. Launch Master Interactive Menu
```bash
python3 run_all.py
```

### 4. Clean Any External CSV Dataset
```bash
python3 -m ai_pair_programming.data_cleaner.main /path/to/dataset.csv
```
