# AI Pair Python Programming — Capstone & Senior Exercise Suite

> **Turnkey Python Engineering Submission**  
> **Standard:** Python 3.8+ (Zero External Dependencies, 0 API Keys, 100% Python Standard Library)

---

## ⚡ Quickstart

This package is completely self-contained. No `pip install`, virtual environment, or external API keys are required.

### 1. Interactive Terminal Launcher
```bash
python3 run_all.py
```
*(Opens an interactive menu allowing 1-click execution of any exercise, capstone, or code review agent)*

### 2. Run Automated Security & Code Bug Review Agent
```bash
python3 code_review_agent.py
```
*(Performs static AST inspection and pattern audits for CWE/OWASP security flaws and runtime bugs)*

### 3. Run All Automated Tests
```bash
python3 test_suite.py
```
*(Executes all 18 unit and integration tests across exercises, data cleaner, code review agent, and E2E pipeline with 100% pass rate)*

---

## 📂 Repository Structure

```text
AI-Pair-Python-Programming/
├── README.md                          # Quickstart guide and documentation (this file)
├── TECHNICAL_DOCUMENTATION.md         # Full algorithmic & engineering specification
├── requirements.txt                   # Standard runtime requirements (0 external dependencies)
├── run_all.py                         # Master interactive terminal launcher
├── code_review_agent.py               # Enterprise AST-based Security & Code Bug Review Agent
├── test_suite.py                      # Master automated test suite runner
├── zip_submission.py                  # Turnkey distribution packager
├── .gitignore                         # Standard git ignore rules
│
├── .github/                           # CI/CD Workflows
│   └── workflows/
│       └── test.yml                   # Automated GitHub Actions test pipeline
│
├── tests/                             # Modular Test Suite (Separate Test Files)
│   ├── __init__.py
│   ├── test_exercises.py              # Tests for Q1–Q10 Python exercises
│   ├── test_data_cleaner.py           # Tests for Capstone Data Cleaning Engine & Custom Datasets
│   ├── test_code_review_agent.py      # Tests for Automated Code Review & Security Agent
│   └── test_e2e.py                    # Tests for End-to-End CSV File I/O & Pipeline
│
├── exercises/                         # Part 1: Senior Python Exercises (Built-in Only)
│   ├── __init__.py
│   ├── q1_unique_elements.py          # Q1: Unique elements with insertion-order preservation
│   ├── q2_perfect_number.py           # Q2: O(sqrt(N)) divisor pair verifier
│   ├── q3_digit_difference.py         # Q3: Digit permutation extrema difference
│   ├── q4_pizza_toppings.py           # Q4: Interactive sentinel prompt loop ('quit')
│   ├── q5_movie_ticket.py             # Q5: Age-tiered pricing loop with input sanitization
│   ├── q6_fibonacci.py                # Q6: Recursive vs Iterative vs Generator Fibonacci
│   ├── q7_pizza_statements.py         # Q7: Iteration & sentence construction formatting
│   ├── q8_square_loop.py              # Q8: Modulo filter with continue flow control
│   ├── q9_anagram_checker.py          # Q9: Anagram theory & O(N) frequency solver
│   └── q10_set_operations.py          # Q10: Set duplicate elimination & operations
│
└── capstone/                          # Part 2: Capstone Project
    ├── __init__.py
    └── data_cleaner/                  # AI-Powered Data Cleaning Assistant
        ├── __init__.py
        ├── cleaner_engine.py          # Missing values, outliers, type inference, deduplication
        ├── reporter.py                # Terminal / Markdown audit report generator
        ├── datasets/                  # Dirty CSV sample datasets
        │   ├── house_prices_dirty.csv
        │   └── ecommerce_orders_dirty.csv
        └── main.py                    # Standalone data cleaner CLI
```

---

## 🧩 Part 1: Python Exercises for Senior Engineers

All 10 questions are implemented with type annotations, docstrings, unit tests, and stand-alone CLI runners:

| # | Question / Module | Algorithm & Highlights | Time | Space |
|---|---|---|---|---|
| **Q1** | [q1_unique_elements.py](file:///usr/local/google/home/arabindaksha/AI-Pair-Python-Programming/exercises/q1_unique_elements.py) | Preserves first-seen insertion order using `dict.fromkeys()` with unhashable fallback. | $O(N)$ | $O(N)$ |
| **Q2** | [q2_perfect_number.py](file:///usr/local/google/home/arabindaksha/AI-Pair-Python-Programming/exercises/q2_perfect_number.py) | Validates sum of proper positive divisors checking divisor pairs up to $\sqrt{N}$. | $O(\sqrt{N})$ | $O(1)$ |
| **Q3** | [q3_digit_difference.py](file:///usr/local/google/home/arabindaksha/AI-Pair-Python-Programming/exercises/q3_digit_difference.py) | Extracts digits, sorts descending & ascending, and calculates difference (e.g. `"213"` $\to 321 - 123 = 198$). | $O(D \log D)$ | $O(D)$ |
| **Q4** | [q4_pizza_toppings.py](file:///usr/local/google/home/arabindaksha/AI-Pair-Python-Programming/exercises/q4_pizza_toppings.py) | Interactive REPL prompt loop with case-insensitive `'quit'` sentinel and automated headless simulator. | $O(1)$/turn | $O(N)$ |
| **Q5** | [q5_movie_ticket.py](file:///usr/local/google/home/arabindaksha/AI-Pair-Python-Programming/exercises/q5_movie_ticket.py) | Age-tiered pricing (<3: Free, 3-12: $10, >12: $15) with `ValueError` recovery and batch simulator. | $O(1)$ | $O(1)$ |
| **Q6** | [q6_fibonacci.py](file:///usr/local/google/home/arabindaksha/AI-Pair-Python-Programming/exercises/q6_fibonacci.py) | Comparative analysis: LRU-memoized recursion ($O(N)$), iterative two-pointer ($O(1)$ space), and lazy generator. | $O(N)$ | $O(1)$ |
| **Q7** | [q7_pizza_statements.py](file:///usr/local/google/home/arabindaksha/AI-Pair-Python-Programming/exercises/q7_pizza_statements.py) | List iteration, statement templating (`"I like {pizza} pizza."`), and concluding multi-line summary. | $O(N)$ | $O(N)$ |
| **Q8** | [q8_square_loop.py](file:///usr/local/google/home/arabindaksha/AI-Pair-Python-Programming/exercises/q8_square_loop.py) | Loops $0..9$, squares numbers, skips even numbers via `continue`, and outputs odd squares ($1, 9, 25, 49, 81$). | $O(N)$ | $O(1)$ |
| **Q9** | [q9_anagram_checker.py](file:///usr/local/google/home/arabindaksha/AI-Pair-Python-Programming/exercises/q9_anagram_checker.py) | Linguistic & mathematical definition + $O(N)$ character frequency map (`collections.Counter`). | $O(N)$ | $O(K)$ |
| **Q10** | [q10_set_operations.py](file:///usr/local/google/home/arabindaksha/AI-Pair-Python-Programming/exercises/q10_set_operations.py) | Set duplicate elimination via Set Union ($A \cup B$) and exclusive items via Symmetric Difference ($A \Delta B$). | $O(N)$ | $O(N)$ |

---

## 🧹 Part 2: Capstone Project — AI-Powered Data Cleaning Assistant

The capstone project is an automated, statistical data-quality pipeline built to clean dirty real-world datasets:

* **Included Sample Datasets:**
  * House Price Prediction Dataset (`capstone/data_cleaner/datasets/house_prices_dirty.csv`)
  * E-Commerce Orders Dataset (`capstone/data_cleaner/datasets/ecommerce_orders_dirty.csv`)
* **Custom Dataset Support:** Accepts any arbitrary `.csv` file provided by the evaluator.
* **4 Core Quality Capabilities:**
  1. **Missing Value Imputation:** Statistical imputation using **Median** (numeric) and **Mode** (categorical).
  2. **Outlier Detection & Capping:** Computes $IQR = Q_3 - Q_1$ fences and bounds anomalies to $[Q_1 - 1.5 \times IQR, Q_3 + 1.5 \times IQR]$.
  3. **Data Type Correction:** Heuristic inference (`int`, `float`, `date`, `str`) with multi-currency sanitization (`$`, `€`, `£`, `¥`).
  4. **Duplicate Detection:** Identifies exact row duplicates and key collisions.
  5. **Executive Audit Report:** Outputs formatted ASCII before/after summary tables and exports clean CSVs.

```bash
# Run interactive cleaner
python3 -m capstone.data_cleaner.main

# Or clean any custom dataset directly
python3 -m capstone.data_cleaner.main /path/to/custom_data.csv
```

---

## 🛡️ Automated Code Review & Security Agent

```bash
python3 code_review_agent.py
```
*(AST-based security vulnerability and defect analyzer verifying 0 dynamic code execution, 0 command injection, and clean code standards)*

---

## 🧪 Running Automated Tests

```bash
# Master runner
python3 test_suite.py

# Run individual test modules
python3 tests/test_exercises.py
python3 tests/test_data_cleaner.py
python3 tests/test_code_review_agent.py
python3 tests/test_e2e.py
```

---

## 📦 Distribution Packager

```bash
python3 zip_submission.py
```
*(Generates `ai_pair_programming_capstone_submission.zip` for final delivery)*
