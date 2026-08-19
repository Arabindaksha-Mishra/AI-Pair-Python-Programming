# AI Pair Python Programming — Capstone & Senior Exercise Suite

> **Turnkey Python Engineering Project**  
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
*(Executes all 21 unit and integration tests across exercises, chatbot, data cleaner, code review agent, and E2E pipeline with 100% pass rate)*

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
│   ├── test_chatbot.py                # Tests for Task 1 Rule-Based Chatbot
│   ├── test_data_cleaner.py           # Tests for Task 2 Data Cleaning Engine & Custom Datasets
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
└── capstone/                          # Part 2: Capstone Projects
    ├── __init__.py
    ├── chatbot/                       # Task 1: Context-Aware Rule-Based Chatbot
    │   ├── __init__.py
    │   ├── regex_matcher.py           # Regex pattern matching & slot extraction
    │   ├── context_memory.py          # Dialogue state & conversation memory tracker
    │   ├── bot_engine.py              # Central response generation engine
    │   └── main.py                    # Standalone interactive chat CLI
    └── data_cleaner/                  # Task 2: Automated Data Cleaning Assistant
        ├── __init__.py
        ├── cleaner_engine.py          # Missing values, outliers, type inference, deduplication
        ├── reporter.py                # Terminal / Markdown audit report generator
        ├── datasets/                  # Dirty CSV sample datasets
        │   ├── house_prices_dirty.csv
        │   └── ecommerce_orders_dirty.csv
        └── main.py                    # Standalone data cleaner CLI
```

---

## 🛡️ Automated Code Review & Security Agent

The repository includes a dedicated static security and bug review agent in [code_review_agent.py](file:///usr/local/google/home/arabindaksha/AI-Pair-Python-Programming/code_review_agent.py):

* **Static AST Code Inspection:** Identifies dangerous dynamic evaluations (`eval`/`exec`), unsafe deserialization (`pickle`), command injection risks (`subprocess` with `shell=True`), and bare `except:` clauses.
* **Pattern & Heuristic Rules:** Flags hardcoded secrets, mutable default arguments, and file path manipulation bugs.
* **Zero Dependencies:** Built 100% using Python built-in modules (`ast`, `re`, `os`, `sys`).

```bash
# Scan workspace
python3 code_review_agent.py
```

---

## 🧪 Running Separate Test Files Individually

Each component has its own dedicated test file in `tests/`:

```bash
# 1. Test Senior Exercises (Q1 to Q10)
python3 tests/test_exercises.py

# 2. Test Rule-Based Chatbot (NLP Regex & State Memory)
python3 tests/test_chatbot.py

# 3. Test Data Cleaning Engine (Type Inference, Imputation, Outliers, Custom CSVs)
python3 tests/test_data_cleaner.py

# 4. Test Code Review Agent Engine
python3 tests/test_code_review_agent.py

# 5. Test End-to-End Pipeline & File Export
python3 tests/test_e2e.py

# 6. Run all tests combined
python3 test_suite.py
```

---

## 📦 Distribution Packager

To package the entire codebase into a clean `.zip` file for distribution:
```bash
python3 zip_submission.py
```
This generates `ai_pair_programming_capstone_submission.zip` ready for evaluation.
