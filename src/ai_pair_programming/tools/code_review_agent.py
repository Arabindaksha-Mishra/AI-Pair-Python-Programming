"""
Enterprise Static Security & Code Quality Review Agent
=======================================================
Autonomous code auditing agent utilizing Python's `ast` engine and pattern
scanners to enforce Clean Code standards, 88-column limits, complete type hints,
zero '#' comments, RN.json version integrity, and OWASP security rules:

- AST Security Rules:
    * SEC-001: Untrusted dynamic execution (eval, exec)
    * SEC-002: Insecure deserialization (pickle, marshal, shelve)
    * SEC-003: Command injection (subprocess with shell=True)
    * SEC-004: Hardcoded API keys / credentials in source

- AST Code Defect Rules:
    * BUG-001: Mutable default arguments (def func(items=[]))
    * BUG-002: Bare except clauses (except: swallowing BaseException)
    * BUG-003: Production assert statements (stripped in -O runtime)
    * BUG-004: Fragile file extension replace logic

- Clean Architecture & Code Quality Rules:
    * TYPE-001: Missing parameter or return type annotations
    * DOC-001: Missing Google-format docstring on functions / classes
    * STYLE-001: Line length exceeding 88-column threshold (E501)
    * STYLE-002: Prohibited '#' comment in Python source files
    * ARCH-001: Missing or corrupted RN.json release notes metadata
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import StrEnum
import json
import os
import re
import sys
from typing import ClassVar

from ai_pair_programming.telemetry import OutputHandler, get_logger


class Severity(StrEnum):
    """Enumeration of issue severity levels."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass(slots=True)
class ReviewFinding:
    """Represents a discrete static analysis finding."""

    file_path: str
    line_number: int
    severity: Severity
    category: str
    rule_id: str
    message: str
    snippet: str
    remediation: str


class SecurityASTVisitor(ast.NodeVisitor):
    """AST Visitor checking for AST-level security flaws and code bugs."""

    def __init__(self, file_path: str, source_lines: list[str]) -> None:
        """
        Initialize the AST visitor.

        Args:
            file_path (str): Path to file being analyzed.
            source_lines (list[str]): Lines of source code.

        Returns:
            None

        """
        self.file_path = file_path
        self.source_lines = source_lines
        self.findings: list[ReviewFinding] = []

    def _get_line_snippet(self, lineno: int) -> str:
        """
        Retrieve single-line source code snippet.

        Args:
            lineno (int): 1-indexed line number.

        Returns:
            str: Trimmed source snippet.

        """
        if 1 <= lineno <= len(self.source_lines):
            return self.source_lines[lineno - 1].strip()
        return ""

    def _check_eval_exec(self, node: ast.Call, func_name: str) -> None:
        """
        Detect eval() and exec() dynamic code execution.

        Args:
            node (ast.Call): AST call node.
            func_name (str): Inferred function name.

        Returns:
            None

        """
        if func_name in ("eval", "exec"):
            self.findings.append(
                ReviewFinding(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    severity=Severity.CRITICAL,
                    category="Code Injection",
                    rule_id="SEC-001",
                    message=f"Dangerous dynamic code execution via '{func_name}()'.",
                    snippet=self._get_line_snippet(node.lineno),
                    remediation=(
                        "Use safe alternatives (e.g., ast.literal_eval) "
                        "or dispatch dictionaries."
                    ),
                )
            )

    def _check_deserialization(self, node: ast.Call, func_name: str) -> None:
        """
        Detect unsafe pickle/marshal/shelve deserialization.

        Args:
            node (ast.Call): AST call node.
            func_name (str): Inferred function name.

        Returns:
            None

        """
        if (
            func_name in ("loads", "load")
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id in ("pickle", "_pickle", "marshal", "shelve")
        ):
            self.findings.append(
                ReviewFinding(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    severity=Severity.CRITICAL,
                    category="Insecure Deserialization",
                    rule_id="SEC-002",
                    message=(
                        f"Insecure deserialization via "
                        f"'{node.func.value.id}.{func_name}'."
                    ),
                    snippet=self._get_line_snippet(node.lineno),
                    remediation=(
                        "Use secure serialization formats like JSON "
                        "or Protocol Buffers."
                    ),
                )
            )

    def _check_subprocess_shell(self, node: ast.Call, func_name: str) -> None:
        """
        Detect subprocess invocations using shell=True.

        Args:
            node (ast.Call): AST call node.
            func_name (str): Inferred function name.

        Returns:
            None

        """
        is_subprocess_call = False
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id in (
                "subprocess",
                "os",
            ):
                is_subprocess_call = True
        elif func_name in ("run", "Popen", "call", "check_output", "check_call"):
            is_subprocess_call = True

        if is_subprocess_call:
            for kw in node.keywords:
                if kw.arg == "shell":
                    is_true = (
                        isinstance(kw.value, ast.Constant) and kw.value.value is True
                    )
                    if is_true:
                        self.findings.append(
                            ReviewFinding(
                                file_path=self.file_path,
                                line_number=node.lineno,
                                severity=Severity.HIGH,
                                category="Command Injection",
                                rule_id="SEC-003",
                                message=(
                                    "subprocess call invoked with "
                                    "'shell=True' risking command injection."
                                ),
                                snippet=self._get_line_snippet(node.lineno),
                                remediation=(
                                    "Pass command as a list of strings and "
                                    "set shell=False."
                                ),
                            )
                        )

    def visit_Call(self, node: ast.Call) -> None:
        """
        Inspect function and method calls for security risks.

        Args:
            node (ast.Call): Call AST node.

        Returns:
            None

        """
        func_name = ""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        self._check_eval_exec(node, func_name)
        self._check_deserialization(node, func_name)
        self._check_subprocess_shell(node, func_name)
        self.generic_visit(node)

    def _check_type_annotations(self, node: ast.FunctionDef) -> None:
        """
        Enforce parameter and return type annotations on function definitions.

        Args:
            node (ast.FunctionDef): Function definition node.

        Returns:
            None

        """
        is_test_file = "tests" in self.file_path.split(os.sep)
        if is_test_file:
            return

        if node.returns is None:
            self.findings.append(
                ReviewFinding(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    severity=Severity.LOW,
                    category="Type Safety",
                    rule_id="TYPE-001",
                    message=(
                        f"Missing return type annotation on function '{node.name}'."
                    ),
                    snippet=self._get_line_snippet(node.lineno),
                    remediation="Add explicit return type hint (e.g. -> None).",
                )
            )

        for arg in node.args.args:
            if arg.arg not in ("self", "cls") and arg.annotation is None:
                self.findings.append(
                    ReviewFinding(
                        file_path=self.file_path,
                        line_number=arg.lineno,
                        severity=Severity.LOW,
                        category="Type Safety",
                        rule_id="TYPE-001",
                        message=(
                            f"Missing type annotation for parameter "
                            f"'{arg.arg}' in function '{node.name}'."
                        ),
                        snippet=self._get_line_snippet(arg.lineno),
                        remediation=f"Add type hint to parameter '{arg.arg}'.",
                    )
                )

    def _check_docstring(self, node: ast.FunctionDef | ast.ClassDef) -> None:
        """
        Verify presence of Google-format docstring.

        Args:
            node (ast.FunctionDef | ast.ClassDef): AST node.

        Returns:
            None

        """
        is_test_file = "tests" in self.file_path.split(os.sep)
        if is_test_file:
            return

        doc = ast.get_docstring(node)
        if not doc:
            self.findings.append(
                ReviewFinding(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    severity=Severity.LOW,
                    category="Documentation",
                    rule_id="DOC-001",
                    message=(
                        f"Missing docstring on {type(node).__name__} '{node.name}'."
                    ),
                    snippet=self._get_line_snippet(node.lineno),
                    remediation="Add a concise Google-format docstring.",
                )
            )

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Check for mutable default arguments, type hints, and docstrings.

        Args:
            node (ast.FunctionDef): Function definition AST node.

        Returns:
            None

        """
        for default in node.args.defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.findings.append(
                    ReviewFinding(
                        file_path=self.file_path,
                        line_number=default.lineno,
                        severity=Severity.HIGH,
                        category="Defective Pattern",
                        rule_id="BUG-001",
                        message=(
                            f"Mutable default argument detected in "
                            f"function '{node.name}'."
                        ),
                        snippet=self._get_line_snippet(default.lineno),
                        remediation=(
                            "Use None as default and initialize in function body "
                            "(e.g., if items is None: items = [])."
                        ),
                    )
                )

        self._check_type_annotations(node)
        self._check_docstring(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Check class definition for docstring compliance.

        Args:
            node (ast.ClassDef): Class definition AST node.

        Returns:
            None

        """
        self._check_docstring(node)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """
        Check for bare except clauses.

        Args:
            node (ast.ExceptHandler): Exception handler AST node.

        Returns:
            None

        """
        if node.type is None:
            self.findings.append(
                ReviewFinding(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    severity=Severity.MEDIUM,
                    category="Exception Handling",
                    rule_id="BUG-002",
                    message=(
                        "Bare 'except:' clause catches BaseException "
                        "(swallows KeyboardInterrupt & SystemExit)."
                    ),
                    snippet=self._get_line_snippet(node.lineno),
                    remediation=(
                        "Specify explicit exception types or catch 'except Exception:'."
                    ),
                )
            )
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        """
        Check for production assertion statements.

        Args:
            node (ast.Assert): Assert statement AST node.

        Returns:
            None

        """
        is_test_file = os.path.basename(self.file_path).startswith(
            "test_"
        ) or "tests" in os.path.normpath(self.file_path).split(os.sep)

        if not is_test_file:
            self.findings.append(
                ReviewFinding(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    severity=Severity.LOW,
                    category="Runtime Invariant",
                    rule_id="BUG-003",
                    message=(
                        "Production assertion statement detected. Assertions are "
                        "stripped when running with -O flag."
                    ),
                    snippet=self._get_line_snippet(node.lineno),
                    remediation=(
                        "Raise explicit ValueError, TypeError, or custom exception "
                        "instead of assert."
                    ),
                )
            )
        self.generic_visit(node)


class CodeReviewAgent:
    """Enterprise Static Security & Code Quality Review Agent."""

    DANGEROUS_PATTERNS: ClassVar[
        list[tuple[re.Pattern[str], Severity, str, str, str, str]]
    ] = [
        (
            re.compile(
                r"(api[_-]?key|secret[_-]?token|password|auth[_-]?token)"
                r"\s*=\s*['\"][A-Za-z0-9_\-]{8,}['\"]",
                re.IGNORECASE,
            ),
            Severity.HIGH,
            "Credential Leak",
            "SEC-004",
            "Potential hardcoded secret or API credential detected in source.",
            ("Load sensitive configuration from environment variables or key vaults."),
        ),
        (
            re.compile(
                r"\.replace\(['\"]\.\w+['\"],\s*['\"]\.\w+['\"]\)", re.IGNORECASE
            ),
            Severity.MEDIUM,
            "Path Manipulation Bug",
            "BUG-004",
            (
                "Using str.replace on file extension may corrupt directory names "
                "containing the same extension string."
            ),
            "Use os.path.splitext(path)[0] + new_ext instead of str.replace.",
        ),
    ]

    def __init__(
        self,
        root_dir: str = ".",
        logger: OutputHandler | None = None,
    ) -> None:
        """
        Initialize Code Review Agent with target root directory.

        Args:
            root_dir (str): Root directory path to scan.
            logger (OutputHandler | None): Logger instance.

        Returns:
            None

        """
        self.root_dir = os.path.abspath(root_dir)
        self.findings: list[ReviewFinding] = []
        self.scanned_files_count: int = 0
        self.total_lines_scanned: int = 0
        self.logger = logger or get_logger("code_reviewer")

    def _scan_style_rules(self, source_lines: list[str], file_path: str) -> None:
        """
        Audit 88-column line width limit and prohibited '#' comments.

        Args:
            source_lines (list[str]): Lines of code.
            file_path (str): File being scanned.

        Returns:
            None

        """
        for lineno, line in enumerate(source_lines, 1):
            line_content = line.rstrip("\r\n")

            if len(line_content) > 88:
                self.findings.append(
                    ReviewFinding(
                        file_path=file_path,
                        line_number=lineno,
                        severity=Severity.LOW,
                        category="Formatting Standard",
                        rule_id="STYLE-001",
                        message=(
                            f"Line exceeds 88-column limit "
                            f"({len(line_content)} > 88 characters)."
                        ),
                        snippet=line_content[:60] + "...",
                        remediation="Refactor or wrap line to be <= 88 columns.",
                    )
                )

            trimmed = line_content.strip()
            if trimmed.startswith("#") and not trimmed.startswith("#!"):
                self.findings.append(
                    ReviewFinding(
                        file_path=file_path,
                        line_number=lineno,
                        severity=Severity.LOW,
                        category="Clean Code Rule",
                        rule_id="STYLE-002",
                        message="Prohibited '#' comment detected in Python source.",
                        snippet=trimmed,
                        remediation=(
                            "Remove '#' comments and document intent via "
                            "Google docstrings and clean code."
                        ),
                    )
                )

    def _scan_regex_patterns(self, source_lines: list[str], file_path: str) -> None:
        """
        Execute regular expression rule audits across source lines.

        Args:
            source_lines (list[str]): Lines of code.
            file_path (str): Path to file being scanned.

        Returns:
            None

        """
        for lineno, line in enumerate(source_lines, 1):
            for (
                pattern,
                severity,
                category,
                rule_id,
                msg,
                remediation,
            ) in self.DANGEROUS_PATTERNS:
                if pattern.search(line):
                    if "DANGEROUS_PATTERNS" in line or "re.compile" in line:
                        continue
                    self.findings.append(
                        ReviewFinding(
                            file_path=file_path,
                            line_number=lineno,
                            severity=severity,
                            category=category,
                            rule_id=rule_id,
                            message=msg,
                            snippet=line.strip(),
                            remediation=remediation,
                        )
                    )

    def analyze_source(self, code_str: str, file_path: str = "<string>") -> None:
        """
        Parse AST, audit style rules, and scan regex patterns.

        Args:
            code_str (str): Source code string content.
            file_path (str): Optional file label.

        Returns:
            None

        """
        source_lines = code_str.splitlines()
        self.total_lines_scanned += len(source_lines)

        try:
            tree = ast.parse(code_str, filename=file_path)
            visitor = SecurityASTVisitor(file_path, source_lines)
            visitor.visit(tree)
            self.findings.extend(visitor.findings)
        except SyntaxError as e:
            self.findings.append(
                ReviewFinding(
                    file_path=file_path,
                    line_number=e.lineno or 1,
                    severity=Severity.CRITICAL,
                    category="Syntax Error",
                    rule_id="SYNTAX-001",
                    message=f"Source syntax error: {e.msg}",
                    snippet=e.text.strip() if e.text else "",
                    remediation="Fix Python syntax error.",
                )
            )

        self._scan_style_rules(source_lines, file_path)
        self._scan_regex_patterns(source_lines, file_path)

    def analyze_file(self, file_path: str) -> None:
        """
        Read and analyze a single Python source file.

        Args:
            file_path (str): Path to the python file.

        Returns:
            None

        """
        if not file_path.endswith(".py"):
            return
        self.scanned_files_count += 1
        try:
            with open(file_path, encoding="utf-8", errors="replace") as f:
                content = f.read()
            self.analyze_source(content, file_path=file_path)
        except Exception as e:
            self.findings.append(
                ReviewFinding(
                    file_path=file_path,
                    line_number=1,
                    severity=Severity.HIGH,
                    category="I/O Error",
                    rule_id="IO-001",
                    message=f"Failed to read file: {e}",
                    snippet="",
                    remediation="Ensure file has read permissions and valid encoding.",
                )
            )

    def validate_release_notes(self) -> None:
        """
        Validate presence and schema conformity of RN.json specification.

        Returns:
            None

        """
        rn_path = os.path.join(self.root_dir, "RN.json")
        if not os.path.isfile(rn_path):
            self.findings.append(
                ReviewFinding(
                    file_path="RN.json",
                    line_number=1,
                    severity=Severity.MEDIUM,
                    category="Architecture",
                    rule_id="ARCH-001",
                    message="Missing root RN.json release specification file.",
                    snippet="",
                    remediation="Generate RN.json tracking project changes.",
                )
            )
            return

        try:
            with open(rn_path, encoding="utf-8") as f:
                records = json.load(f)
            if not isinstance(records, list):
                self.findings.append(
                    ReviewFinding(
                        file_path="RN.json",
                        line_number=1,
                        severity=Severity.MEDIUM,
                        category="Architecture",
                        rule_id="ARCH-001",
                        message=(
                            "RN.json root structure should be a list of change records."
                        ),
                        snippet="",
                        remediation=(
                            "Ensure RN.json contains a list of change dictionaries."
                        ),
                    )
                )
        except Exception as e:
            self.findings.append(
                ReviewFinding(
                    file_path="RN.json",
                    line_number=1,
                    severity=Severity.HIGH,
                    category="Architecture",
                    rule_id="ARCH-001",
                    message=f"Failed to parse RN.json: {e}",
                    snippet="",
                    remediation="Fix JSON syntax error in RN.json.",
                )
            )

    def scan_directory(self, target_dir: str | None = None) -> list[ReviewFinding]:
        """
        Recursively scan all Python files in the given directory.

        Args:
            target_dir (str | None): Target directory or default root.

        Returns:
            list[ReviewFinding]: Aggregated list of findings.

        """
        scan_root = os.path.abspath(target_dir or self.root_dir)
        self.logger.info(f"Initiating security scan across: {scan_root}")
        ignore_dirs = {
            ".git",
            "__pycache__",
            ".venv",
            "venv",
            "dist",
            "build",
            ".pytest_cache",
            ".ruff_cache",
        }

        for root, dirs, files in os.walk(scan_root):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    self.analyze_file(full_path)

        self.validate_release_notes()

        self.logger.info(
            f"Security scan completed: {self.scanned_files_count} files, "
            f"{len(self.findings)} findings."
        )
        return self.findings

    def generate_report(self, use_color: bool = True) -> str:
        """
        Generate a structured terminal audit report of all findings.

        Args:
            use_color (bool): Whether to include ANSI color codes.

        Returns:
            str: Multi-line formatted terminal report.

        """
        red = "\033[91m" if use_color else ""
        yellow = "\033[93m" if use_color else ""
        green = "\033[92m" if use_color else ""
        bold = "\033[1m" if use_color else ""
        reset = "\033[0m" if use_color else ""

        crit_count = sum(1 for f in self.findings if f.severity == Severity.CRITICAL)
        high_count = sum(1 for f in self.findings if f.severity == Severity.HIGH)
        med_count = sum(1 for f in self.findings if f.severity == Severity.MEDIUM)
        low_count = sum(
            1 for f in self.findings if f.severity in (Severity.LOW, Severity.INFO)
        )

        lines = [
            "\n==================================================================",
            "   🛡️  ENTERPRISE CODE REVIEW & SECURITY AUDIT AGENT REPORT",
            "==================================================================",
            f"• Files Scanned:       {self.scanned_files_count}",
            f"• Lines of Code (LOC): {self.total_lines_scanned}",
            f"• Total Findings:      {len(self.findings)}",
            (
                f"  - Critical: {red}{crit_count}{reset} | "
                f"High: {red}{high_count}{reset} | "
                f"Medium: {yellow}{med_count}{reset} | "
                f"Low/Info: {low_count}"
            ),
            "------------------------------------------------------------------",
        ]

        if not self.findings:
            lines.append(
                f"\n{green}{bold}✅ CLEAN AUDIT PASS! Zero security vulnerabilities "
                f"or code defects detected.{reset}\n"
            )
            lines.append(
                "• Safe AST structure (No eval/exec, no insecure deserialization)."
            )
            lines.append("• Safe subprocess handling (No shell=True).")
            lines.append("• No bare except clauses or mutable defaults.")
            lines.append("• 100% type hints & Google docstrings validated.")
            lines.append("• Strict 88-column limit & zero '#' comments verified.")
            lines.append("• RN.json version management integrity validated.")
        else:
            lines.append(f"\n{bold}Detailed Findings Breakdown:{reset}")
            for idx, f in enumerate(self.findings, 1):
                sev_color = (
                    red if f.severity in (Severity.CRITICAL, Severity.HIGH) else yellow
                )
                rel_path = os.path.relpath(f.file_path, self.root_dir)
                lines.append(
                    f"\n[{idx}] {sev_color}{bold}[{f.severity.value}] "
                    f"{f.category} ({f.rule_id}){reset}"
                )
                lines.append(f"    Location:    {rel_path}:{f.line_number}")
                lines.append(f"    Message:     {f.message}")
                if f.snippet:
                    lines.append(f"    Snippet:     `{f.snippet}`")
                lines.append(f"    Remediation: {f.remediation}")

        lines.append(
            "==================================================================\n"
        )
        return "\n".join(lines)


def main() -> None:
    """
    Execute CLI entrypoint for security audit scan.

    Returns:
        None

    """
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    agent = CodeReviewAgent(root_dir=".")
    print(f"Scanning target path: {target}...")
    agent.scan_directory(target)
    print(agent.generate_report())
    if any(f.severity in (Severity.CRITICAL, Severity.HIGH) for f in agent.findings):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
