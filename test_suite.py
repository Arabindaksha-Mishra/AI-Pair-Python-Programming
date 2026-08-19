#!/usr/bin/env python3
"""
Master Automated Test Suite
===========================
Unified runner executing all modular test suites:
- tests/test_exercises.py    : Part 1 — Senior Python Exercises (Q1 to Q10)
- tests/test_chatbot.py      : Part 2 (Task 1) — Context-Aware Rule-Based Chatbot
- tests/test_data_cleaner.py : Part 2 (Task 2) — Automated Data Cleaning Assistant
- tests/test_e2e.py          : End-to-End Pipeline & File I/O Integration

Run via:
    python3 test_suite.py
    or
    python3 -m unittest discover tests
"""

import sys
import unittest

# Import separate test suites
from tests.test_exercises import TestSeniorExercises
from tests.test_chatbot import TestRuleBasedChatbot
from tests.test_data_cleaner import TestDataCleaningAssistant
from tests.test_e2e import TestDataCleaningPipelineE2E
from tests.test_code_review_agent import TestCodeReviewAgent


def run_all_tests() -> unittest.TestResult:
    """Discovers and runs all modular test suites."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestSeniorExercises))
    suite.addTests(loader.loadTestsFromTestCase(TestRuleBasedChatbot))
    suite.addTests(loader.loadTestsFromTestCase(TestDataCleaningAssistant))
    suite.addTests(loader.loadTestsFromTestCase(TestDataCleaningPipelineE2E))
    suite.addTests(loader.loadTestsFromTestCase(TestCodeReviewAgent))

    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    result = run_all_tests()
    sys.exit(0 if result.wasSuccessful() else 1)

