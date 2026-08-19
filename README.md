# AI Pair Python Programming — Senior Capstone & Exercise Suite

> **Evaluation-Ready Turnkey Submission**  
> **Standard:** Python 3.8+ (Zero External Dependencies, 0 API Keys, 100% Python Built-ins)

---

## ⚡ 1-Minute Trainer Quickstart

This package is completely self-contained. No `pip install`, virtual environment, or external API keys are required.

### 1. Run the Interactive Launcher (Recommended)
```bash
python3 run_all.py
```
*(Opens an interactive terminal menu allowing 1-click execution of any exercise or capstone project)*

### 2. Run the Automated Test Suite
```bash
python3 test_suite.py
```
*(Executes all 15 unit tests covering algorithms, edge cases, regex patterns, and data cleaning routines with 100% pass rate)*

---

## 📂 Project Architecture

```text
ai_pair_programming_capstone/
├── README.md                          # Quickstart guide & documentation (this file)
├── TECHNICAL_DOCUMENTATION.md         # Full engineering & algorithmic specification
├── run_all.py                         # Master interactive terminal launcher
├── test_suite.py                      # Automated unit tests (100% pass rate)
├── zip_submission.py                  # Single-command packager for zip distribution
├── exercises/                         # Part 1: Senior Python Exercises (Built-in Only)
│   ├── __init__.py
│   ├── q1_unique_elements.py          # Q1: Unique list with order preservation
│   ├── q2_perfect_number.py           # Q2: O(sqrt(N)) perfect number verifier
│   ├── q3_digit_difference.py         # Q3: Digit permutation extrema difference
│   ├── q4_pizza_toppings.py           # Q4: Interactive sentinel prompt loop
│   ├── q5_movie_ticket.py             # Q5: Age-tiered pricing loop with input sanitization
│   ├── q6_fibonacci.py                # Q6: Recursive vs Iterative vs Generator Fibonacci
│   ├── q7_pizza_statements.py         # Q7: Iteration & sentence construction formatting
│   ├── q8_square_loop.py              # Q8: Modulo filter with continue flow control
│   ├── q9_anagram_checker.py          # Q9: Anagram theory & O(N) frequency solver
│   └── q10_set_operations.py          # Q10: Set duplicate elimination & operations
└── capstone/                          # Part 2: Capstone Projects
    ├── __init__.py
    ├── chatbot/                       # Task 1: Context-Aware Rule-Based Chatbot
    │   ├── __init__.py
    │   ├── regex_matcher.py           # Regex patterns & intent/entity extraction
    │   ├── context_memory.py          # Dialogue state & conversation memory tracker
    │   ├── bot_engine.py              # Central response generation engine
    │   └── main.py                    # Standalone interactive chat CLI
    └── data_cleaner/                  # Task 2: Automated Data Cleaning Assistant
        ├── __init__.py
        ├── cleaner_engine.py          # Missing values, outliers, type inference, deduplication
        ├── reporter.py                # Markdown/Terminal audit report generator
        ├── datasets/                  # Sample dirty datasets (CSV)
        │   ├── house_prices_dirty.csv
        │   └── ecommerce_orders_dirty.csv
        └── main.py                    # Standalone data cleaner CLI
```

---

## 🧩 Part 1: Python Exercises for Senior Engineers

All 10 questions are implemented with type annotations, docstrings, unit tests, and stand-alone CLI runners:

| # | Question / Module | Algorithm & Engineering Highlights | Time | Space |
|---|---|---|---|---|
| **Q1** | `exercises/q1_unique_elements.py` | Preserves first-seen insertion order using `dict.fromkeys()` with unhashable fallback. | $O(N)$ | $O(N)$ |
| **Q2** | `exercises/q2_perfect_number.py` | Validates sum of proper positive divisors checking divisor pairs up to $\sqrt{N}$. | $O(\sqrt{N})$ | $O(1)$ |
| **Q3** | `exercises/q3_digit_difference.py` | Extracts digits, sorts descending & ascending, and calculates difference (e.g. `"213"` $\to 321 - 123 = 198$). | $O(D \log D)$ | $O(D)$ |
| **Q4** | `exercises/q4_pizza_toppings.py` | Interactive REPL prompt loop with case-insensitive `'quit'` sentinel and automated headless simulator. | $O(1)$/turn | $O(N)$ |
| **Q5** | `exercises/q5_movie_ticket.py` | Age-tiered pricing (<3: Free, 3-12: $10, >12: $15) with `ValueError` recovery and batch simulator. | $O(1)$ | $O(1)$ |
| **Q6** | `exercises/q6_fibonacci.py` | Comparative analysis: LRU-memoized recursion ($O(N)$), iterative two-pointer ($O(1)$ space), and lazy generator. | $O(N)$ | $O(1)$ |
| **Q7** | `exercises/q7_pizza_statements.py` | List iteration, statement templating (`"I like {pizza} pizza."`), and concluding multi-line summary. | $O(N)$ | $O(N)$ |
| **Q8** | `exercises/q8_square_loop.py` | Loops $0..9$, squares numbers, skips even numbers via `continue`, and outputs odd squares ($1, 9, 25, 49, 81$). | $O(N)$ | $O(1)$ |
| **Q9** | `exercises/q9_anagram_checker.py` | Full linguistic & mathematical definition + $O(N)$ character frequency map (`collections.Counter`). | $O(N)$ | $O(K)$ |
| **Q10** | `exercises/q10_set_operations.py` | Set duplicate elimination via Set Union ($A \cup B$) and exclusive items via Symmetric Difference ($A \Delta B$). | $O(N)$ | $O(N)$ |

---

## 🤖 Part 2: Capstone Projects

### Task 1: Context-Aware Rule-Based Chatbot (`capstone/chatbot/`)
* **Pattern Matching with Regular Expressions (`re`):** Multi-tier regex matching for greetings, farewells, help, identity, time, and exercise queries.
* **Context Awareness & State Machine:** Remembers the user's name, previous intent, turn count, and last discussed topics across conversation turns.
* **Categorized Responses:** Segregated dynamic response templates for greetings, questions, farewells, gratitude, and graceful fallbacks.
* **How to run:**
  ```bash
  python3 -m capstone.chatbot.main
  ```

---

### Task 2: Automated Data Cleaning Assistant (`capstone/data_cleaner/`)
* **Why "AI-Powered"?** Uses statistical anomaly modeling ($Z$-scores & $IQR$ distribution fences) and heuristic inference to prepare raw datasets for ML training without external APIs or heavy C-dependencies.
* **Core Capabilities:**
  1. **Missing Value Imputation:** Imputes numeric features using median and categorical features using mode.
  2. **Outlier Detection & Capping:** Computes $IQR = Q_3 - Q_1$ fences and bounds anomalies.
  3. **Data Type Correction:** Parses dirty currencies (`"$450,000"`, `"-50,000"`), ISO dates, and numeric strings.
  4. **Duplicate Detection:** Identifies exact row duplicates and primary key collisions.
  5. **Audit Reporter:** Generates before & after ASCII/Markdown health score tables.
* **How to run:**
  ```bash
  python3 -m capstone.data_cleaner.main
  ```

---

## 📦 How to Create the Submission Zip
To package the entire codebase into a clean, submission-ready `.zip` file:
```bash
python3 zip_submission.py
```
This generates `ai_pair_programming_capstone_submission.zip` ready for distribution.
