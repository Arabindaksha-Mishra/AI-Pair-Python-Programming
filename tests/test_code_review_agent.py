"""
Test Suite: Automated Code Review & Security Agent
===================================================
Unit tests verifying detection of AST flaws, dangerous patterns, and clean pass scenarios.
"""

import os
import sys
import tempfile
import unittest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from code_review_agent import CodeReviewAgent, Severity


class TestCodeReviewAgent(unittest.TestCase):
    """Tests for CodeReviewAgent security and defect inspection."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.agent = CodeReviewAgent(root_dir=self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_detect_eval_and_exec(self):
        test_file = os.path.join(self.temp_dir.name, "bad_injection.py")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("def run_untrusted(user_str):\n    return eval(user_str)\n")

        self.agent.analyze_file(test_file)
        eval_findings = [f for f in self.agent.findings if f.rule_id == "SEC-001"]
        self.assertTrue(len(eval_findings) >= 1)
        self.assertEqual(eval_findings[0].severity, Severity.CRITICAL)

    def test_detect_mutable_default_argument(self):
        test_file = os.path.join(self.temp_dir.name, "bad_default.py")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("def append_item(val, items=[]):\n    items.append(val)\n    return items\n")

        self.agent.analyze_file(test_file)
        def_findings = [f for f in self.agent.findings if f.rule_id == "BUG-001"]
        self.assertTrue(len(def_findings) >= 1)
        self.assertEqual(def_findings[0].severity, Severity.HIGH)

    def test_detect_bare_except(self):
        test_file = os.path.join(self.temp_dir.name, "bad_except.py")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("try:\n    x = 1 / 0\nexcept:\n    pass\n")

        self.agent.analyze_file(test_file)
        except_findings = [f for f in self.agent.findings if f.rule_id == "BUG-002"]
        self.assertTrue(len(except_findings) >= 1)
        self.assertEqual(except_findings[0].severity, Severity.MEDIUM)

    def test_clean_file_passes(self):
        test_file = os.path.join(self.temp_dir.name, "clean_code.py")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("def add(a: int, b: int) -> int:\n    return a + b\n")

        self.agent.analyze_file(test_file)
        self.assertEqual(len(self.agent.findings), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
