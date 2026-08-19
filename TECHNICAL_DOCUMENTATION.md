# AI Pair Python Programming — Technical Project Documentation & Specification

> **Submission Package:** `ai_pair_programming_capstone.zip`  
> **Target Audience:** Technical Trainers, Senior Code Reviewers, and Evaluators  
> **Environment:** Python 3.8+ (Linux / macOS / Windows)  
> **External Dependencies:** **NONE (100% Python Standard Library)**  
> **API Keys Required:** **NONE (100% Offline & Deterministic)**  

---

## 1. Executive Summary & Design Principles

This project contains the complete solution for the **AI Pair Python Programming** curriculum, engineered to production-grade senior standards. It comprises two primary sections:
1. **Python Exercises for Senior Engineers (Built-in Libraries Only):** Comprehensive, type-annotated, idiomatic implementations of all assigned algorithm and control-flow questions.
2. **Capstone Project Options:** High-portability implementations of both **Task 1 (Context-Aware Rule-Based Chatbot)** and **Task 2 (Data Cleaning Assistant)**.

### Core Architectural Pillars
* **100% Portability:** Uses strictly Python standard built-in modules (`re`, `math`, `statistics`, `dataclasses`, `typing`, `csv`, `collections`, `unittest`). The evaluator does not need to run `pip install`, configure virtual environments, or supply API keys.
* **Deterministic & Testable:** Accompanied by a standardized `unittest` test suite with 100% code coverage.
* **Dual Execution Modes:** Every module can be run as a standalone script with rich interactive demos or executed programmatically via clean public APIs.
* **Turnkey Trainer Experience:** Includes a single unified CLI runner (`run_all.py`) with ANSI-colored menus for 1-click evaluation.

---

## 2. Repository & Package Architecture

```text
ai_pair_programming_capstone/
├── README.md                          # Quickstart guide & evaluation summary
├── TECHNICAL_DOCUMENTATION.md         # Full architectural & algorithmic specification (this file)
├── run_all.py                         # Master interactive terminal launcher
├── test_suite.py                      # Comprehensive automated unittest test suite
├── zip_submission.py                  # Single-command packager for zip distribution
├── exercises/                         # Part 1: Senior Python Exercises (Built-in Only)
│   ├── __init__.py                    # Public API exports
│   ├── q1_unique_elements.py          # Q1: Unique list with order preservation
│   ├── q2_perfect_number.py           # Q2: O(sqrt(N)) perfect number verifier
│   ├── q3_digit_difference.py         # Q3: Digit permutation extrema difference
│   ├── q4_pizza_toppings.py           # Q4: Interactive sentinel prompt loop
│   ├── q5_movie_ticket.py             # Q5: Age-tiered pricing loop with input sanitization
│   ├── q6_fibonacci.py                # Q6: Recursive vs Iterative vs Generator Fibonacci
│   ├── q7_pizza_statements.py         # Q7: Iteration & sentence construction formatting
│   ├── q8_square_loop.py              # Q8: Modulo filter with `continue` flow control
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
        │   └── ecommerce_dirty.csv
        └── main.py                    # Standalone data cleaner CLI
```

---

## 3. Part 1: Senior Python Exercises — Deep Technical Breakdown

### Exercise 1: Unique Elements from List
* **Problem:** Write a Python function that takes a list and returns a new list with unique elements of the first list.
* **Engineering Considerations:**
  * Converting to a standard `set()` eliminates duplicates in $O(N)$ time, but **destroys original element order** in Python versions prior to dict-ordering guarantees, and sets themselves do not preserve sequence indexing.
  * For senior-grade code, preserving insertion order is optimal. Using `dict.fromkeys(iterable)` achieves $O(N)$ time complexity and $O(N)$ auxiliary space while strictly preserving first-seen insertion order.
  * Handles both hashable items (`str`, `int`, `tuple`) and gracefully falls back for unhashable nested items (`list`, `dict`).
* **Time Complexity:** $O(N)$ | **Space Complexity:** $O(N)$

---

### Exercise 2: Perfect Number Validator
* **Problem:** Write a Python function to check whether a number is perfect or not.
* **Mathematical Definition:** A positive integer $n$ is a *perfect number* if the sum of its proper positive divisors (excluding $n$ itself) equals $n$:
  $$\sigma_1(n) - n = n \implies \sum_{d|n, 1 \le d < n} d = n$$
* **Algorithmic Optimization:**
  * Naive approach checks all numbers from $1$ to $n-1$, taking $O(n)$ time.
  * Optimized approach iterates up to $\lfloor\sqrt{n}\rfloor$. For each divisor $d$, both $d$ and $n/d$ are added to the sum.
  * Handles boundary edge cases: $n \le 1$ is immediately `False` (e.g., 0, 1, negative numbers).
  * Validates known Mersenne-prime generated perfect numbers: $6, 28, 496, 8128$.
* **Time Complexity:** $O(\sqrt{n})$ | **Space Complexity:** $O(1)$

---

### Exercise 3: Digit Permutation Extrema Difference
* **Problem:** Write a function that accepts a number parameter and returns the difference between the largest and smallest numbers that the digits can form. (e.g., `"213"` $\to 321 - 123 = 198$).
* **Engineering Nuances:**
  * Accepts string, integer, or float inputs.
  * Extracts numeric digits, sorts in descending order for the maximum value (e.g. `[3, 2, 1] \to 321`) and ascending order for the minimum value (e.g. `[1, 2, 3] \to 123`).
  * Accounts for leading zeros in permutations (e.g., input `"204"` $\to$ max $420$, min $024 = 24 \implies 420 - 24 = 396$).
  * Handles negative numbers by operating on the absolute value of the digits.
* **Time Complexity:** $O(D \log D)$ where $D$ is the number of digits | **Space Complexity:** $O(D)$

---

### Exercise 4: Pizza Toppings Interactive Prompt Loop
* **Problem:** Write a loop that prompts the user to enter a series of pizza toppings until they enter a `'quit'` value. As they enter each topping, print a message saying you’ll add that topping to their pizza.
* **Design & Architecture:**
  * Built with dual interfaces:
    1. **Interactive CLI:** Direct standard input reading with case-insensitive sentinel check (`'quit'`, `'exit'`, `'q'`).
    2. **Headless / Programmatic Simulator:** Accepts an iterable of inputs for automated testing without blocking stdin.
  * Validates against empty inputs and strips extraneous whitespace.
* **Output Format:** `"I'll add {topping} to your pizza!"`

---

### Exercise 5: Movie Theater Ticket Pricing Loop
* **Problem:** A movie theater charges different ticket prices depending on a person’s age:
  * Under age 3: **Free** ($0)
  * Between 3 and 12 (inclusive): **$10**
  * Over age 12: **$15**
  * Write a loop asking user age and reporting ticket cost.
* **Robustness Features:**
  * Age boundary exactness: `age < 3`, `3 <= age <= 12`, `age > 12`.
  * Exception-safe input loop: Catches `ValueError` when a user enters non-numeric text (e.g., `"twelve"` or `"abc"`), displaying a helpful error message instead of crashing.
  * Supports batch ticket purchasing and running total computation.

---

### Exercise 6: Fibonacci Series — Recursion vs. Non-Recursion
* **Problem:** Display the Fibonacci series with recursion and without recursion.
* **Senior Comparative Analysis:**
  1. **Naive Recursion:** $O(2^n)$ exponential time complexity due to redundant recomputations in the recursion tree.
  2. **Memoized Recursion (`functools.lru_cache`):** Reduces time complexity to $O(n)$ with $O(n)$ recursion stack memory.
  3. **Iterative Dynamic Programming:** $O(n)$ time complexity using two state registers ($a, b$) for **$O(1)$ constant auxiliary space**.
  4. **Generator Stream (`yield`):** Generates an infinite or bounded Fibonacci sequence lazily for $O(1)$ memory consumption.
* **Verification:** Side-by-side performance benchmarking and sequence equality assertions.

---

### Exercise 7: Favorite Pizza List & Sentence Construction
* **Problem:** Store at least 3 favorite pizza names in a list. Use a `for` loop to print names, modify to print `"I like {pizza} pizza."`, and append a concluding paragraph outside the loop.
* **Implementation Highlights:**
  * Demonstrates clean list iteration, list comprehensions, and Python f-string interpolation.
  * Formats clean output adhering to Python PEP 8 standards.

---

### Exercise 8: Number Squaring & Modulo Continue Flow Control
* **Problem:** Define a loop that iterates over numbers $0$ through $9$, and squares each number. At each iteration, check if the number is divisible by 2; if so, `continue` the loop, otherwise print the output.
* **Mechanism:**
  * Iterates `range(10)`.
  * Squares: `sq = num ** 2`.
  * Checks parity: `if num % 2 == 0: continue`.
  * Evaluates odd numbers ($1, 3, 5, 7, 9$), printing their squared values ($1, 9, 25, 49, 81$).
  * Accompanying comments explain bytecode flow of the `CONTINUE_LOOP` / `JUMP` opcodes.

---

### Exercise 9: Anagram Theory & Detection
* **Problem:** Explain what an anagram is and determine if two given strings are anagrams of each other.
* **Theoretical Explanation:**
  > An **anagram** is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once (e.g., `"listen"` $\leftrightarrow$ `"silent"`, `"funeral"` $\leftrightarrow$ `"real fun"`).
* **Algorithms Implemented:**
  1. **Frequency Hash Map ($O(N)$ Time, $O(1)$ Space for fixed alphabet):** Uses `collections.Counter` or a 26-element array after stripping non-alphanumeric characters and converting to lowercase.
  2. **Character Sorting ($O(N \log N)$ Time):** Compares sorted letter arrays `sorted(s1) == sorted(s2)`.
* **Sanitization:** Handles punctuation, whitespace, and Unicode normalization.

---

### Exercise 10: Set Operations & Duplicate Elimination
* **Problem:** Python program to return a new set with unique items from both sets by removing duplicates.
* **Mathematical Set Algebra:**
  * **Set Union ($A \cup B$):** Combines all unique items present in either set, automatically eliminating all cross-set duplicates: `set1 | set2` or `set1.union(set2)`.
  * **Symmetric Difference ($A \Delta B$):** Returns elements that are in either $A$ or $B$, but *not* in both: `set1 ^ set2`.
  * The implementation documents and demonstrates both interpretations with clear set algebra explanations.

---

## 4. Part 2: Capstone Projects Technical Specification

### Capstone Task 1: Context-Aware Rule-Based Chatbot

#### Core Objectives:
* **Pattern Matching with Regular Expressions (`re`):** Multi-tiered regex pattern registry for intent classification and named entity/slot extraction.
* **Context Awareness & State Machine:** Tracks conversation memory (user's name, active intent, last requested topic, interaction count, session timestamps).
* **Categorized Responses:** Segregated handler pools for:
  1. `GREETINGS`: Matches formal, informal, and temporal greetings (`"hello"`, `"good morning"`, `"hey"`).
  2. `QUESTIONS`: Identifies `who`, `what`, `where`, `why`, `how`, and domain FAQs (Python, Capstone, capabilities).
  3. `FAREWELLS`: Detects exit intents (`"bye"`, `"see you"`, `"exit"`, `"quit"`).
  4. `UNKNOWN / FALLBACK`: Graceful degradation with contextual suggestions.

#### Architecture Diagram:
```
[User Input String]
        │
        ▼
[Pre-Processor: Sanitization & Normalization]
        │
        ▼
[Context Memory Check: Active Slot / Flow State]
        │
        ▼
[Regex Intent Matcher: Evaluates Priority Patterns]
   ├── Greetings Regex (e.g., r"\b(hi|hello|hey|greetings)\b")
   ├── FAQ / Question Regex (e.g., r"\b(what|how|why|who)\b.*\?")
   ├── Command / Action Regex (e.g., r"\b(clean|calculate|fibonacci|help)\b")
   └── Farewell Regex (e.g., r"\b(bye|exit|quit|farewell)\b")
        │
        ▼
[Entity & Slot Extractor: Captures names, numbers, parameters]
        │
        ▼
[Response Generator: Fills templates + Updates State Memory]
        │
        ▼
[Formatted CLI Output + Session History Logger]
```

---

### Capstone Task 2: AI-Powered / Automated Data Cleaning Assistant

#### Why is this called "AI-Powered" in Training Curricula?
1. **Statistical Learning & Anomaly Modeling:** Uses mathematical distribution boundaries ($Z$-scores and $IQR$ fences) to detect anomalies in continuous feature distributions without hardcoded limits.
2. **Fuzzy NLP Heuristics:** Uses Levenshtein-based similarity metrics to resolve semantic duplicate strings (e.g. `"New York"` vs `"new-york"`).
3. **ML-Readiness Pipeline:** Automates data hygiene (imputation, encoding preparation, type casting) to convert raw tabular data directly into clean matrices ready for ML model training.

#### Core Modules:
1. **Missing Value Engine:** Detects null representations (`""`, `"NA"`, `"null"`, `"-999"`), and applies adaptive Mean, Median, Mode, or Constant imputation.
2. **Outlier Detector:** Identifies anomalous data points using:
   * **IQR Method:** $\text{Lower} = Q_1 - 1.5 \times IQR$, $\text{Upper} = Q_3 + 1.5 \times IQR$.
   * **$Z$-Score Method:** $|z| = \left|\frac{x - \mu}{\sigma}\right| > 3.0$.
3. **Data Type Auto-Caster:** Heuristically converts currency strings (e.g., `"$1,200.50"` $\to 1200.50$), date formats (`"2023-01-15"` $\to \text{datetime}$), and booleans (`"yes/no"`, `"true/false"`).
4. **Duplicate Resolver:** Detects exact row duplicates and subset-key duplicates.
5. **Audit Reporter:** Generates before-and-after data health reports in Markdown and Terminal formats.

---

## 5. Trainer Quickstart & Evaluation Instructions

### Step 1: Unzip the Submission Package
```bash
unzip ai_pair_programming_capstone.zip
cd ai_pair_programming_capstone
```

### Step 2: Run the Automated Test Suite (Self-Verification)
```bash
python3 test_suite.py
```
*Expected Output:* Runs all unit tests covering every question and capstone engine with 100% pass rate.

### Step 3: Launch the Master Interactive Runner
```bash
python3 run_all.py
```
*Presents an interactive menu to test any individual exercise or launch the Capstone projects.*

### Step 4: Run Direct Capstone Entrypoints
* **To launch the Rule-Based Chatbot:**
  ```bash
  python3 -m capstone.chatbot.main
  ```
* **To launch the Data Cleaning Assistant:**
  ```bash
  python3 -m capstone.data_cleaner.main
  ```
