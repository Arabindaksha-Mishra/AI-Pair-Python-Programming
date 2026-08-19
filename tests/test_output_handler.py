"""
Test Suite: Centralized Output & Structured Logging Handler
============================================================
Unit tests covering log levels, formatting, ANSI colorization, file emission,
1-hour rotating file handlers, and pipeline telemetry tracking.
"""

from __future__ import annotations

import logging
import os
import sys
import tempfile
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from ai_pair_programming.telemetry import (
    ColorLogFormatter,
    OutputHandler,
    get_logger,
    get_logs_directory,
)


class TestOutputHandler(unittest.TestCase):
    """Unit tests for OutputHandler logging and telemetry module."""

    def setUp(self) -> None:
        """
        Set up temporary sandbox directory fixture for log files.

        Returns:
            None

        """
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        """
        Clean up temporary test sandbox.

        Returns:
            None

        """
        self.temp_dir.cleanup()

    def test_output_handler_instantiation(self) -> None:
        """
        Verify instantiation with default parameters and custom log levels.

        Returns:
            None

        """
        handler = OutputHandler(
            name="test_logger",
            level=logging.DEBUG,
            enable_hourly_file=False,
        )
        self.assertEqual(handler.logger.name, "test_logger")
        self.assertEqual(handler.logger.level, logging.DEBUG)

    def test_file_logging(self) -> None:
        """
        Verify logging output routed directly to a file on disk.

        Returns:
            None

        """
        log_file = os.path.join(self.temp_dir.name, "app.log")
        handler = OutputHandler(
            name="file_logger", level=logging.INFO, log_file=log_file
        )

        handler.info("Informational message for test")
        handler.warning("Warning message for test")

        self.assertTrue(os.path.exists(log_file))
        with open(log_file, encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Informational message for test", content)
        self.assertIn("Warning message for test", content)

    def test_hourly_rotating_file_handler(self) -> None:
        """
        Verify 1-hour interval rotating file handler configuration.

        Returns:
            None

        """
        log_file = os.path.join(self.temp_dir.name, "hourly.log")
        handler = OutputHandler(
            name="hourly_logger",
            level=logging.INFO,
            enable_hourly_file=False,
        )
        handler.add_hourly_rotating_file_handler(log_file, backup_hours=24)
        handler.info("Hourly rotating log entry")

        self.assertTrue(os.path.exists(log_file))
        with open(log_file, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Hourly rotating log entry", content)

    def test_color_formatter(self) -> None:
        """
        Verify ANSI color decoration on formatted LogRecords.

        Returns:
            None

        """
        formatter = ColorLogFormatter(fmt="%(levelname)s: %(message)s")
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="hello world",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        self.assertIn("hello world", formatted)
        self.assertIn(ColorLogFormatter.GREEN, formatted)

    def test_log_transformation_step(self) -> None:
        """
        Verify telemetry logging method for dataset transformation steps.

        Returns:
            None

        """
        log_file = os.path.join(self.temp_dir.name, "telemetry.log")
        handler = OutputHandler(
            name="telemetry_logger", level=logging.INFO, log_file=log_file
        )

        handler.log_transformation_step("OutlierRemoval", 100, 95)

        with open(log_file, encoding="utf-8") as f:
            content = f.read()

        self.assertIn("OutlierRemoval", content)
        self.assertIn("In: 100", content)
        self.assertIn("Out: 95", content)
        self.assertIn("Delta: -5", content)

    def test_get_logger_singleton(self) -> None:
        """
        Verify get_logger factory function returns a valid OutputHandler.

        Returns:
            None

        """
        logger = get_logger("singleton_test", enable_hourly_file=False)
        self.assertIsInstance(logger, OutputHandler)

    def test_get_logs_directory(self) -> None:
        """
        Verify resolution of the logs directory.

        Returns:
            None

        """
        logs_dir = get_logs_directory()
        self.assertTrue(os.path.exists(logs_dir))
        self.assertTrue(logs_dir.endswith("logs"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
