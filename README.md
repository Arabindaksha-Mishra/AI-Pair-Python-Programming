# 🚀 AI Pair Python Programming — Capstone & Senior Suite

> **Automated Data Quality Remediation & Senior Python Engineering Solutions**  
> Python 3.12+ Standard Library | Zero External Dependencies  
> **100% CI Quality Gate Pass** | **48 Unit & Integration Tests** | **AST Validated**

---

## 1. Task 2: AI-Powered Data Cleaning Assistant

The primary objective of **Task 2 (AI-Powered Data Cleaning Assistant)** is to
automatically detect and resolve common data quality anomalies in structured
datasets (such as *House Price Prediction* and *E-Commerce Transaction* datasets),
transforming raw, dirty tabular data into analysis- and modeling-ready matrices.

The pipeline executes a deterministic 4-stage data remediation workflow:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   TASK 2 DATA QUALITY REMEDIATION PIPELINE             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
    1. Data Type Correction         ▼
    ┌────────────────────────────────────────────────────────────────────┐
    │ • Multi-currency stripping ($1,250.00, €45.50 -> 1250.0, 45.5)     │
    │ • Accounting parenthesized negatives ((250.00) -> -250.0)          │
    │ • ISO-8601 Date Standardization (15/01/2024, 01-15-2024 -> YYYY-MM)│
    │ • Heuristic Native Type Casting (int, float, bool, str, None)      │
    └───────────────────────────────┬────────────────────────────────────┘
                                    │
    2. Duplicate Detection          ▼
    ┌────────────────────────────────────────────────────────────────────┐
    │ • Full-row exact duplicate identification                          │
    │ • Order-preserving matrix row deduplication                        │
    │ • Optional primary key collision filtering                         │
    └───────────────────────────────┬────────────────────────────────────┘
                                    │
    3. Missing Value Imputation     ▼
    ┌────────────────────────────────────────────────────────────────────┐
    │ • Universal null token detection ("", "n/a", "none", "nan", "-999")│
    │ • Numeric Columns: Column-level Median statistical replacement     │
    │ • Categorical Columns: Column-level Mode frequency replacement     │
    └───────────────────────────────┬────────────────────────────────────┘
                                    │
    4. Outlier Detection & Capping  ▼
    ┌────────────────────────────────────────────────────────────────────┐
    │ • Tukey's IQR Fences: [Q1 - 1.5*IQR, Q3 + 1.5*IQR]                 │
    │ • Non-destructive Winsorization upper/lower boundary capping       │
    │ • Preserves total sample size without distorting distribution      │
    └───────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
                     Remediated ML-Ready Tabular Dataset
```

### 1.1 Data Type Correction & Value Sanitization
* **Location**: `src/ai_pair_programming/data_transformer/sanitizer.py`
* **Mechanism**:
  - **Null Token Recognition**: Inspects raw cells against `NULL_STRINGS` (`""`,
    `"n/a"`, `"na"`, `"null"`, `"none"`, `"nan"`, `"-999"`, `"?"`, `"nil"`,
    `"undefined"`, `"missing"`).
  - **Financial Currency Parsing**: Strips international currency symbols (`$`,
    `€`, `£`, `¥`), removes thousands commas, and resolves accounting-style
    negative parenthesized strings (`(500)` $\to$ `-500.0`).
  - **Date Normalization**: Standardizes non-uniform date strings (`DD/MM/YYYY`,
    `MM/DD/YYYY`, `YYYY/MM/DD`, `DD-MM-YYYY`) into ISO-8601 `YYYY-MM-DD`.
  - **Heuristic Type Casting**: Casts strings into appropriate native Python
    primitives (`int`, `float`, `bool`, or `None`).

### 1.2 Duplicate Detection & Removal
* **Location**: `src/ai_pair_programming/data_transformer/deduplicator.py`
* **Mechanism**:
  - Performs order-preserving duplicate row filtering in $\mathcal{O}(N)$ time.
  - Converts serialized cell values into immutable hashed row representations.
  - Supports both full-row exact deduplication and primary-key index filtering.

### 1.3 Missing Value Detection & Statistical Imputation
* **Location**: `src/ai_pair_programming/data_transformer/imputer.py`
* **Mechanism**:
  - Scans all column vectors for standard and non-standard missing values.
  - **Continuous Numeric Features**: Computes and substitutes the column **Median**
    (resistant to extreme outliers).
  - **Discrete Categorical Features**: Computes and substitutes the column **Mode**
    (most frequent category), falling back to constant defaults if empty.

### 1.4 Outlier Detection & Winsorization
* **Location**: `src/ai_pair_programming/data_transformer/outlier_handler.py`
* **Mechanism**:
  - Calculates Interquartile Range ($IQR = Q_3 - Q_1$) across numeric features.
  - Computes Tukey outlier fences:
    $$\text{Lower} = Q_1 - 1.5 \times IQR, \quad \text{Upper} = Q_3 + 1.5 \times IQR$$
  - Applies **Winsorization**: Caps extreme values exceeding the fences to the
    respective boundary thresholds, preserving sample size without skewing models.

---

## 2. Task 1: Senior Python Exercises (7 Question Sets)

The repository provides comprehensive, fully tested standard library implementations
for the 7 foundational Senior Python Exercise questions in
`src/ai_pair_programming/exercises/`:

### 2.1 Question 1: Unique Elements & Deduplication (`unique_elements.py`)
- **`unique_elements(items)`**: Performs $\mathcal{O}(N)$ order-preserving list
  deduplication without altering element sequence.
- **`set_union_and_difference(set_a, set_b)`**: Demonstrates set algebra by returning
  the mathematical union ($A \cup B$) and difference ($A \setminus B$).

### 2.2 Question 2: Perfect Number Validation (`perfect_number.py`)
- **`is_perfect_number(n)`**: Efficient $\mathcal{O}(\sqrt{N})$ square-root factor
  summation algorithm to verify if a positive integer equals the sum of its proper
  divisors (e.g., $6 = 1 + 2 + 3$, $28 = 1 + 2 + 4 + 7 + 14$).
- **`find_perfect_numbers_in_range(start, end)`**: Discovers all perfect numbers
  bounded within an arbitrary numeric interval.

### 2.3 Question 3: Digit Extremes & Difference (`digit_difference.py`)
- **`digit_difference(number)`**: Computes the numerical difference between the
  maximum and minimum integer permutations formed by the digits of a number
  (e.g., input `2149` $\to 9421 - 1249 = 8172$).
- **`get_digit_extremes(number)`**: Returns the maximum and minimum permutations.

### 2.4 Question 4: Fibonacci Sequence Implementations (`fibonacci_series.py`)
- **`fibonacci_iterative(n)`**: Generates first $n$ Fibonacci numbers in
  $\mathcal{O}(N)$ time and $\mathcal{O}(N)$ space.
- **`fibonacci_recursive(n)`**: Computes $n$-th Fibonacci value using memoization.
- **`fibonacci_generator(limit)`**: Memory-efficient generator yielding Fibonacci
  values lazily with $\mathcal{O}(1)$ auxiliary space.

### 2.5 Question 5: Anagram Detection & Frequency Matching (`anagram_solver.py`)
- **`are_anagrams_sorted(str1, str2)`**: Canonical character sorting with case
  insensitivity and whitespace stripping.
- **`are_anagrams_frequency(str1, str2)`**: Linear $\mathcal{O}(N)$ character frequency
  counting algorithm using hash maps.
- **`explain_anagram(str1, str2)`**: Generates human-readable anagram audit reports.

### 2.6 Question 6: Movie Ticket Age-Tiered Pricing (`movie_tickets.py`)
- **`calculate_movie_ticket_price(age)`**: Tiered price calculation function
  (Age $< 3$: Free `$0.00`, Age $3\text{--}12$: `$10.00`, Age $> 12$: `$15.00`).
- **`movie_tickets_repl()`**: Interactive terminal console loop supporting 'quit'
  sentinels and graceful input validation.

### 2.7 Question 7: Interactive Loops & Pizza Statements (`interactive_loops.py`)
- **`pizza_toppings_repl()`**: Interactive `while True` loop prompting for toppings
  until the `'quit'` sentinel is entered.
- **`square_even_continue_loop(numbers)`**: Loops through integers, skipping odd
  values via `continue` and returning squares of even values.
- **`format_pizza_statements(pizzas)`**: Generates templated descriptive sentences
  using idiomatic list comprehension.

---

## 3. Before & After Pipeline Transformation

### Raw Input Matrix (Dirty E-Commerce / House Price Dataset)
| ID | Area (sqft) | Price (Raw) | Sale Date | Status |
| :--- | :--- | :--- | :--- | :--- |
| `"101"` | `"1500"` | `"$450,000.00"` | `"2024-01-15"` | `"active"` |
| `"102"` | `"-999"` | `"$500,000.00"` | `"15/01/2024"` | `"null"` |
| `"103"` | `"12000"` | `"($50,000.00)"` | `"2024/01/16"` | `"pending"` |
| `"101"` | `"1500"` | `"$450,000.00"` | `"2024-01-15"` | `"active"` |

### Remediated Output Matrix (Cleaned & ML-Ready)
| ID | Area (sqft) | Price (Float) | Sale Date (ISO) | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `101` | `1500` | `450000.0` | `"2024-01-15"` | `"active"` | Typed & parsed |
| `102` | `1500` | `500000.0` | `"2024-01-15"` | `"active"` | Imputed values |
| `103` | `3200` | `-50000.0` | `"2024-01-16"` | `"pending"`| Winsorized |

*(Duplicate record dropped, missing area imputed with median 1500, outlier area
capped to upper fence 3200).*

---

## 4. Directory & Package Architecture

```text
AI-Pair-Python-Programming/
├── main.py                          # Master Application CLI Entrypoint
├── tests.py                         # Master Modular Test Suite Runner (48 Tests)
├── pyproject.toml                   # Packaging & Tooling Config (Ruff / uv)
├── release_notes.json               # Enterprise Change Tracking Database
├── README.md                        # Task 1 & 2 Engineering Specification
├── CI/                              # Continuous Integration Quality Gates
│   ├── run_quality_checks.py        # Master CI Pipeline Runner
│   ├── check_line_length.py         # 88-Column Line Width Checker
│   ├── check_no_hash_comments.py    # Prohibited Hash Comment Auditor
│   └── validate_release_notes.py    # release_notes.json Schema Validator
├── src/ai_pair_programming/         # Source Root Package
│   ├── __init__.py                  # Top-Level Package Exports & Models
│   ├── models.py                    # Dataclass Models & Type Aliases
│   ├── constants.py                 # Global Constants & RegEx Patterns
│   ├── exceptions.py                # Domain Exceptions Hierarchy
│   ├── exercises/                   # Task 1 Senior Exercises Subpackage
│   │   ├── __init__.py              # Exercises Re-exports
│   │   ├── unique_elements.py       # Q1: Unique elements & deduplication
│   │   ├── perfect_number.py        # Q2: Perfect numbers & range search
│   │   ├── digit_difference.py      # Q3: Digit permutation max-min
│   │   ├── fibonacci_series.py      # Q4: Fibonacci series & generator
│   │   ├── anagram_solver.py        # Q5: Anagram detection & frequency
│   │   ├── movie_tickets.py         # Q6: Age-tiered ticket pricing REPL
│   │   ├── interactive_loops.py     # Q7: Interactive loops & continue
│   │   ├── collections_ops.py       # Collection operations utility
│   │   └── numeric_math.py          # Primes & mathematical algorithms
│   ├── capstone/                    # Task 2 Data Quality Assistant Subpackage
│   │   ├── cleaner_engine.py        # DataCleaningAssistant Orchestrator
│   │   ├── reporter.py              # Cleaning Audit Report Generator
│   │   └── transformer/             # Subpackage Re-exports
│   ├── data_transformer/            # Core Reusable Transformation Engine
│   │   ├── sanitizer.py             # Type Inference & Currency Parsing
│   │   ├── imputer.py               # Missing Value Statistical Imputation
│   │   ├── outlier_handler.py       # IQR Fences & Winsorization Capping
│   │   ├── deduplicator.py          # Exact & Key-Based Deduplication
│   │   └── io_utils.py              # Robust Standard Library CSV I/O
│   ├── telemetry/                   # Logging & Observability Engine
│   │   └── output_handler.py        # ANSI Colored & 1-Hour Rotating Logger
│   └── tools/                       # Developer & Governance Tools
│       ├── code_review_agent.py     # AST Security & Defect Inspection Agent
│       └── version_manager.py       # release_notes.json Tracking Engine
└── tests/                           # Unit & Integration Test Suites
    ├── test_exercises.py            # Task 1 Exercise Tests (7 Modules)
    ├── test_data_transformer.py     # Transformation Engine Tests
    ├── test_data_cleaner.py         # Capstone Engine Tests
    ├── test_models.py               # Data Models Tests
    ├── test_constants_exceptions.py # Constants & Exception Tests
    ├── test_output_handler.py       # Telemetry Logging Tests
    ├── test_code_review_agent.py    # Security Agent Tests
    ├── test_version_manager.py      # Version Manager Tests
    └── test_e2e.py                  # End-to-End Pipeline Integration Tests
```

---

## 5. Programmatic API Usage Example

```python
from ai_pair_programming import (
    CleaningConfig,
    DataCleaningAssistant,
    TabularDataset,
    get_logger,
)

# 1. Initialize Logger
logger = get_logger("pipeline")

# 2. Configure Remediation Parameters
config = CleaningConfig(
    iqr_factor=1.5,
    z_score_threshold=3.0,
    numeric_impute_strategy="median",
    categorical_impute_strategy="mode",
)

# 3. Instantiate Assistant & Remediate Matrix
cleaner = DataCleaningAssistant(config=config, logger=logger)
cleaned_headers, cleaned_rows = cleaner.clean_dataset(
    headers=["id", "area", "price", "sale_date"],
    rows=[
        ["101", "1500", "$450,000.00", "2024-01-15"],
        ["102", "-999", "$500,000.00", "15/01/2024"],
        ["101", "1500", "$450,000.00", "2024-01-15"],
    ],
)

# 4. Wrap in Strongly-Typed Dataclass
dataset = TabularDataset(headers=cleaned_headers, rows=cleaned_rows)
print(f"Remediated Matrix Shape: {dataset.shape}")  # (2, 4)
```

---

## 6. Domain Models, Constants & Exceptions

### 6.1 Dataclass Models (`models.py`)
- `PrimitiveValue`: `str | int | float | bool | None` scalar union type.
- `RawCellValue`: `object` unvalidated input representation.
- `CastResult`: `tuple[PrimitiveValue, str]` (value, type_name) tuple.
- `TabularRow`: `list[PrimitiveValue]` row cell vector.
- `TabularMatrix`: `list[TabularRow]` 2D table matrix.
- `TabularDataset`: Strongly-typed dataset container with `.shape`, `.num_rows`.
- `CleaningConfig`: Pipeline configuration dataclass.
- `ReleaseRecord`: Version tracking model for `release_notes.json`.

### 6.2 Central Constants (`constants.py`)
- `DEFAULT_IQR_FACTOR`: `1.5`
- `DEFAULT_Z_SCORE_THRESHOLD`: `3.0`
- `DEFAULT_NUMERIC_IMPUTE_STRATEGY`: `"median"`
- `DEFAULT_CATEGORICAL_IMPUTE_STRATEGY`: `"mode"`
- `NULL_STRINGS`: `frozenset({"", "n/a", "na", "null", "none", "nan", "-999"})`
- `SUPPORTED_DATE_FORMATS`: `("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d")`
- `MAX_LINE_LENGTH`: `88`

### 6.3 Domain Exceptions (`exceptions.py`)
```text
AIPairProgrammingError (Base Exception)
├── DataCleanerError (Capstone Errors)
│   ├── DatasetValidationError
│   ├── ColumnNotFoundError
│   └── FileProcessingError
└── VersionManagerError (Versioning Errors)
    └── ReleaseNotesSchemaError
```

---

## 7. Static AST Review & Security Scanner Rules

- `SEC-001` (CRITICAL): Dynamic code execution via `eval()` or `exec()`.
- `SEC-002` (CRITICAL): Unsafe deserialization via `pickle` or `marshal`.
- `SEC-003` (HIGH): Subprocess invocation with `shell=True`.
- `SEC-004` (HIGH): Hardcoded API keys or secrets in source code.
- `SEC-005` (HIGH): Race condition vulnerability in `tempfile.mktemp()`.
- `BUG-001` (HIGH): Mutable default arguments (`def f(items=[])`).
- `BUG-002` (MEDIUM): Bare `except:` catching `BaseException`.
- `BUG-003` (LOW): Production `assert` statement stripped in `-O`.
- `BUG-004` (MEDIUM): Fragile file extension replacement logic.
- `BUG-005` (MEDIUM): Identity check (`is`/`is not`) on primitive literal.
- `STYLE-001` (LOW): Line length exceeding 88-column limit (E501).
- `STYLE-002` (LOW): Prohibited `#` comment in Python source files.

---

## 8. Execution & Verification Commands

```bash
# 1. Run Interactive CLI application
python3 main.py

# 2. Run master test suite (48 unit and integration tests)
python3 tests.py

# 3. Run static AST security and defect scanner
PYTHONPATH=src python3 -m ai_pair_programming.tools.code_review_agent

# 4. Run master CI quality gate verification
python3 CI/run_quality_checks.py
```
