"""
Test Suite: Automated Code Review & Security Agent
===================================================
Unit tests verifying detection of AST flaws, dangerous patterns,
style rules, and clean passes.
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from ai_pair_programming.tools.code_review_agent import CodeReviewAgent, Severity


class TestCodeReviewAgent(unittest.TestCase):
    """Tests for CodeReviewAgent security and defect inspection."""

    def setUp(self) -> None:
        """
        Set up temporary sandbox directory and agent instance.

        Returns:
            None

        """
        self.temp_dir = tempfile.TemporaryDirectory()
        self.agent = CodeReviewAgent(root_dir=self.temp_dir.name)

    def tearDown(self) -> None:
        """
        Clean up temporary test sandbox.

        Returns:
            None

        """
        self.temp_dir.cleanup()

    def test_detect_eval_and_exec(self) -> None:
        """
        Verify detection of SEC-001 eval/exec code injection.

        Returns:
            None

        """
        test_file = os.path.join(self.temp_dir.name, "bad_injection.py")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(
                "def run_untrusted(user_str: str) -> None:\n"
                '    """Run eval."""\n'
                "    eval(user_str)\n"
            )

        self.agent.analyze_file(test_file)
        eval_findings = [f for f in self.agent.findings if f.rule_id == "SEC-001"]
        self.assertTrue(len(eval_findings) >= 1)
        self.assertEqual(eval_findings[0].severity, Severity.CRITICAL)

    def test_detect_mutable_default_argument(self) -> None:
        """
        Verify detection of BUG-001 mutable default arguments.

        Returns:
            None

        """
        test_file = os.path.join(self.temp_dir.name, "bad_default.py")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(
                "def append_item(val: int, items: list = []) -> list:\n"
                '    """Append item."""\n'
                "    items.append(val)\n"
                "    return items\n"
            )

        self.agent.analyze_file(test_file)
        def_findings = [f for f in self.agent.findings if f.rule_id == "BUG-001"]
        self.assertTrue(len(def_findings) >= 1)
        self.assertEqual(def_findings[0].severity, Severity.HIGH)

    def test_detect_bare_except(self) -> None:
        """
        Verify detection of BUG-002 bare except swallowing exceptions.

        Returns:
            None

        """
        test_file = os.path.join(self.temp_dir.name, "bad_except.py")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(
                "def divide_zero() -> None:\n"
                '    """Divide zero."""\n'
                "    try:\n"
                "        x = 1 / 0\n"
                "    except:\n"
                "        pass\n"
            )

        self.agent.analyze_file(test_file)
        bare_findings = [f for f in self.agent.findings if f.rule_id == "BUG-002"]
        self.assertTrue(len(bare_findings) >= 1)
        self.assertEqual(bare_findings[0].severity, Severity.MEDIUM)

    def test_detect_style_violations(self) -> None:
        """
        Verify detection of line length and prohibited hash comments.

        Returns:
            None

        """
        test_file = os.path.join(self.temp_dir.name, "bad_style.py")
        long_line = "x = '" + ("a" * 100) + "'"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(
                f"# Prohibited comment\n"
                f"def bad_func() -> None:\n"
                f'    """Bad function."""\n'
                f"    {long_line}\n"
            )

        self.agent.analyze_file(test_file)
        style_findings = [
            f for f in self.agent.findings if f.rule_id in ("STYLE-001", "STYLE-002")
        ]
        self.assertTrue(len(style_findings) >= 2)

    def test_clean_file_passes(self) -> None:
        """
        Verify clean, defect-free files pass with zero findings.

        Returns:
            None

        """
        test_file = os.path.join(self.temp_dir.name, "clean_code.py")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(
                "def add_numbers(a: int, b: int) -> int:\n"
                '    """\n'
                "    Add two numbers.\n"
                "\n"
                "    Args:\n"
                "        a (int): First.\n"
                "        b (int): Second.\n"
                "\n"
                "    Returns:\n"
                "        int: Sum.\n"
                "\n"
                '    """\n'
                "    return a + b\n"
            )

        self.agent.analyze_file(test_file)
        self.assertEqual(len(self.agent.findings), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
