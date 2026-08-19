# Enterprise Coding Standards & Readability Guidelines

> **Based on Uncle Bob's Clean Code Principles & Modern Python 3.12+ Standards**  
> **Target Audience:** All Engineers, Reviewers, and AI Assistants

---

## 1. Executive Summary & Core Philosophy

Writing software that merely "works" is only the first step. To maintain
long-term agility, reliability, and maintainability, all code written in this
repository must adhere to the **Clean Code & Readability** principles
established in Uncle Bob's *Clean Code* and adapted for modern Python 3.12+.

> *"Truth can only be found in one place: the code. Don't use comments to*
> *cover up bad code — rewrite it into clean, self-explanatory functions."*

---

## 2. Docstrings over Comments & Function Decomposition

### 🚫 Rule 1: Zero `#` Inline & Section Comments
- **No `#` comments in source code:** `#` inline comments and section dividers
  are prohibited across all Python modules.
- **Self-Documenting Code:** If code requires a comment to explain *what* it
  is doing, that block must be extracted into a dedicated helper function.

### 🧩 Rule 2: Single Level of Abstraction & Function Decomposition (F4)
- **Small Functions:** Functions should ideally be 5–20 lines, performing one
  task completely at a single level of abstraction.
- **Extract Multi-Step Blocks:** Replace procedural multi-step pipelines with
  composed subroutines:
  ```python
  # Decomposed functions with docstrings and type hints
  def clean_dataset(rows: list[list[str]]) -> DatasetProfile:
      """
      Execute multi-phase cleaning pipeline.

      Args:
          rows (list[list[str]]): Raw matrix rows.

      Returns:
          DatasetProfile: Sanitized profile container.

      """
      sanitized = _sanitize_rows(rows)
      inferred_types = _infer_column_types(sanitized)
      deduped = _deduplicate_records(sanitized)
      imputed = _impute_missing_values(deduped, inferred_types)
      return _cap_outliers(imputed, inferred_types)
  ```

### 📜 Rule 3: Standardized Google Docstring Format
Every function, method, constructor, and class must follow the format:
- A clear, concise summary line describing what the function does.
- An `Args:` section listing each argument `name (type): description`.
- A `Returns:` section detailing `type: description` (or `None`).
- An optional `Raises:` section documenting errors raised.
- Concise, balanced length (neither overly verbose nor terse).

```python
def is_empty_string_or_none(data: str) -> bool:
    """
    Check if the data is an 'empty string' or 'None'.

    Args:
        data (str): The data to check.

    Returns:
        bool: True if the supplied data is 'None', or if it only contains
            an empty string "".

    """
    if data is None or data == "":
        return True
    return False
```

---

## 3. Core Clean Code Heuristics & Rules

### 1. Functions & Signatures
* **F1: Maximum 3 Arguments:** Keep argument lists small (0–2 ideal, 3 max).
  Bundle related inputs into `@dataclass(slots=True)` containers.
* **F2: No Output Arguments:** Functions should return new transformed objects
  rather than mutating passed arguments in place.
* **F3: No Flag Arguments:** Avoid `def process(is_admin: bool)`. Split into
  distinct functions: `process_admin()` and `process_standard()`.
* **F4: Single Responsibility Principle (SRP):** Each function has 1 purpose.

### 2. Meaningful Naming (N1 – N7)
* **Intention-Revealing:** A variable or function name should tell you why it
  exists and what it does without needing comments.
* **Searchable & Pronounceable:** No single-letter variables except short loop
  indices (`i`, `j`) or mathematical coordinates (`x`, `y`).
* **Explicit Side-Effects:** If a function modifies state or caches to disk,
  make it explicit (`get_and_cache_dataset` vs `get_dataset`).

### 3. Error Handling & Boundaries
* **G3: Test Boundary Conditions:** Rigorously verify `0`, `-1`, empty `[]`,
  `None`, and maximum extrema.
* **G25: Replace Magic Numbers:** Replace literal numbers with named constants
  (`SECONDS_PER_DAY = 86_400`).
* **G28: Encapsulate Conditionals:** Extract complex boolean expressions into
  predicate helper methods (`if is_eligible():`).
* **Safe Exceptions:** Never catch bare `except:`; specify precise types.

---

## 4. Python 3.12+ Language & Formatting Standards

* **📏 Mandatory 88-Column Maximum Line Length (`E501`):** Every line of
  code, docstring, comment, and document must be strictly within 88 columns.
* **🏷️ Mandatory Complete Type Hints (`ANN`):** Every function, method, and
  `__init__` constructor must have explicit type annotations.
* **PEP 604 Pipe Unions:** Use `str | None` instead of `Optional[str]`.
* **PEP 585 Built-in Collections:** Use `list[T]`, `dict[K, V]` directly.
* **Abstract Collections:** Import `Iterable`, `Generator` from `collections.abc`.
* **Dataclasses:** Use `@dataclass(slots=True)` for pure data objects.
* **Single-Step Tooling:**
  - Automated tests: `python3 test_suite.py` (1 command, 100% pass).
  - Code review scan: `python3 -m ai_pair_programming.tools.code_review_agent`.
  - Strict Formatter: `ruff check --fix . && ruff format .` (1 command).

---

## 5. Architectural Layering

```text
src/ai_pair_programming/
├── algorithms/         -> Mathematical, string, loop, and collection ops
├── data_transformer/   -> Reusable sanitizers, deduplicators, imputers
├── data_cleaner/       -> High-level tabular data cleaning engine & CLI
└── tools/              -> AST-based static code review agent & packager
```

---

## 6. Review Checklist for All Python Modules

Before committing or submitting any code:
- [ ] Are all docstrings conforming to standardized Google `Args:`/`Returns:`?
- [ ] Are all `#` comments removed, with logic explained by function names?
- [ ] Is every single line strictly $\le 88$ columns wide?
- [ ] Does every function and method have complete, explicit type annotations?
- [ ] Are large multi-step functions broken down into small helpers?
- [ ] Are all function argument counts $\le 3$?
- [ ] Are boolean selector / flag arguments eliminated?
- [ ] Are all magic numbers replaced with named constants?
- [ ] Do unit tests pass with 100% coverage via `python3 test_suite.py`?
- [ ] Does the AST security scanner report 0 findings?
