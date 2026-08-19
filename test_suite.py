#!/usr/bin/env python3
"""
Master Automated Test Suite (uv / src Standard)
===============================================
Unified runner executing all modular test suites:
- tests/test_algorithms.py        : Part 1 — Domain Groups 1 to 4
- tests/test_data_transformer.py  : Core Reusable Data Transformer Package
- tests/test_data_cleaner.py      : Part 2 — Automated Data Cleaning Assistant
- tests/test_output_handler.py    : Centralized Logging & Telemetry Engine
- tests/test_e2e.py               : End-to-End Pipeline & File I/O Integration
- tests/test_code_review_agent.py : Static AST & Security Inspection Agent
- tests/test_version_manager.py   : RN.json Release Notes & Version Manager

Run via:
    python3 test_suite.py
    or
    python3 -m unittest discover tests
"""

from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from tests.test_algorithms import TestSeniorAlgorithms
from tests.test_code_review_agent import TestCodeReviewAgent
from tests.test_data_cleaner import TestDataCleaningAssistant
from tests.test_data_transformer import TestDataTransformer
from tests.test_e2e import TestDataCleaningPipelineE2E
from tests.test_output_handler import TestOutputHandler
from tests.test_version_manager import TestVersionManager


def run_all_tests() -> unittest.TestResult:
    """
    Discover and execute all modular unit and integration test suites.

    Returns:
        unittest.TestResult: Test execution summary result object.

    """
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestSeniorAlgorithms))
    suite.addTests(loader.loadTestsFromTestCase(TestDataTransformer))
    suite.addTests(loader.loadTestsFromTestCase(TestDataCleaningAssistant))
    suite.addTests(loader.loadTestsFromTestCase(TestOutputHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestDataCleaningPipelineE2E))
    suite.addTests(loader.loadTestsFromTestCase(TestCodeReviewAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestVersionManager))

    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    result = run_all_tests()
    sys.exit(0 if result.wasSuccessful() else 1)
