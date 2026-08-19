"""
Structured Logging & Telemetry Engine
=====================================
Unified output handler providing colorized console streaming and automated
1-hour interval rotating file logging into the centralized `logs/` directory.
"""

from __future__ import annotations

import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys
from typing import ClassVar


def _resolve_project_logs_dir() -> str:
    """
    Locate or create the root 'logs' directory for the project.

    Returns:
        str: Absolute filesystem path to the 'logs' directory.

    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    logs_dir = os.path.join(project_root, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir


class ColorLogFormatter(logging.Formatter):
    """Custom formatter injecting ANSI color codes into terminal log records."""

    GREY: ClassVar[str] = "\x1b[38;20m"
    GREEN: ClassVar[str] = "\x1b[32;20m"
    YELLOW: ClassVar[str] = "\x1b[33;20m"
    RED: ClassVar[str] = "\x1b[31;20m"
    BOLD_RED: ClassVar[str] = "\x1b[31;1m"
    RESET: ClassVar[str] = "\x1b[0m"

    LEVEL_COLORS: ClassVar[dict[int, str]] = {
        logging.DEBUG: GREY,
        logging.INFO: GREEN,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: BOLD_RED,
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Format LogRecord instance with severity-specific ANSI escape codes.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: Colorized multi-line log string.

        """
        color = self.LEVEL_COLORS.get(record.levelno, self.RESET)
        formatted = super().format(record)
        return f"{color}{formatted}{self.RESET}"


class OutputHandler:
    """
    Unified logger with console streaming and 1-hour interval file rotation.
    """

    DEFAULT_FORMAT: ClassVar[str] = (
        "%(asctime)s | %(levelname)-8s | %(name)s : %(message)s"
    )
    DATE_FORMAT: ClassVar[str] = "%Y-%m-%d %H:%M:%S"

    def __init__(
        self,
        name: str = "ai_pair_programming",
        level: int = logging.INFO,
        log_file: str | None = None,
        enable_hourly_file: bool = True,
        use_color: bool = True,
    ) -> None:
        """
        Initialize the OutputHandler with console and hourly file handlers.

        Args:
            name (str): Logger namespace identifier.
            level (int): Minimum logging severity level.
            log_file (str | None): Optional specific path for log output.
            enable_hourly_file (bool): Whether to log to hourly rotating file.
            use_color (bool): Whether to enable ANSI console colors.

        Returns:
            None

        """
        env_level = os.environ.get("LOG_LEVEL", "").upper()
        if env_level in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            level = getattr(logging, env_level)

        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False
        self._configure_handlers(level, log_file, enable_hourly_file, use_color)

    def _configure_handlers(
        self,
        level: int,
        log_file: str | None,
        enable_hourly_file: bool,
        use_color: bool,
    ) -> None:
        """
        Configure console stream and 1-hour interval rotating file handlers.

        Args:
            level (int): Logging severity level threshold.
            log_file (str | None): Explicit file path destination.
            enable_hourly_file (bool): Flag to attach rotating hourly file.
            use_color (bool): Color formatting flag.

        Returns:
            None

        """
        if self.logger.handlers:
            self.logger.handlers.clear()

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        if use_color and sys.stdout.isatty():
            console_formatter = ColorLogFormatter(
                fmt=self.DEFAULT_FORMAT, datefmt=self.DATE_FORMAT
            )
        else:
            console_formatter = logging.Formatter(
                fmt=self.DEFAULT_FORMAT, datefmt=self.DATE_FORMAT
            )

        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        if log_file:
            self.add_file_handler(log_file, level)
        elif enable_hourly_file and os.environ.get("DISABLE_FILE_LOGS") != "1":
            default_log_dir = _resolve_project_logs_dir()
            default_log_path = os.path.join(default_log_dir, "app.log")
            self.add_hourly_rotating_file_handler(default_log_path, level=logging.DEBUG)

    def add_hourly_rotating_file_handler(
        self,
        log_file: str,
        level: int = logging.DEBUG,
        backup_hours: int = 168,
    ) -> None:
        """
        Attach a 1-hour interval rotating file handler.

        Rotates every hour (when='h', interval=1) and retains historical
        hourly logs up to backup_hours (default: 168 hours / 7 days).

        Args:
            log_file (str): Base file path destination.
            level (int): Minimum severity level for the file handler.
            backup_hours (int): Number of historical hourly files to retain.

        Returns:
            None

        """
        log_dir = os.path.dirname(os.path.abspath(log_file))
        os.makedirs(log_dir, exist_ok=True)

        file_handler = TimedRotatingFileHandler(
            filename=log_file,
            when="h",
            interval=1,
            backupCount=backup_hours,
            encoding="utf-8",
            delay=True,
        )
        file_handler.suffix = "%Y-%m-%d_%H"
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            fmt=self.DEFAULT_FORMAT, datefmt=self.DATE_FORMAT
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def add_file_handler(self, log_file: str, level: int = logging.DEBUG) -> None:
        """
        Attach a static non-rotating file handler.

        Args:
            log_file (str): Filesystem path to the destination log file.
            level (int): Minimum severity level for the file handler.

        Returns:
            None

        """
        log_dir = os.path.dirname(os.path.abspath(log_file))
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            fmt=self.DEFAULT_FORMAT, datefmt=self.DATE_FORMAT
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def debug(self, msg: str) -> None:
        """
        Emit a diagnostic debug log event.

        Args:
            msg (str): Message text describing internal state.

        Returns:
            None

        """
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        """
        Emit an informational log event for milestone progress.

        Args:
            msg (str): Informational milestone message.

        Returns:
            None

        """
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        """
        Emit a warning log event for non-fatal irregularities.

        Args:
            msg (str): Warning notification text.

        Returns:
            None

        """
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        """
        Emit an error log event for recoverable exceptions.

        Args:
            msg (str): Error message string.

        Returns:
            None

        """
        self.logger.error(msg)

    def critical(self, msg: str) -> None:
        """
        Emit a critical log event for unrecoverable pipeline halts.

        Args:
            msg (str): Critical fault description.

        Returns:
            None

        """
        self.logger.critical(msg)

    def log_transformation_step(
        self, step_name: str, records_in: int, records_out: int
    ) -> None:
        """
        Record a structured pipeline transformation telemetry entry.

        Args:
            step_name (str): Label of the transformation phase.
            records_in (int): Count of incoming records.
            records_out (int): Count of transformed outgoing records.

        Returns:
            None

        """
        delta = records_out - records_in
        self.logger.info(
            f"Step: {step_name:<20} | In: {records_in:<6} | "
            f"Out: {records_out:<6} | Delta: {delta:+d}"
        )


_LOGGERS: dict[str, OutputHandler] = {}


def get_logs_directory() -> str:
    """
    Get the default directory path where hourly rotated logs are stored.

    Returns:
        str: Absolute filesystem path to 'logs' directory.

    """
    return _resolve_project_logs_dir()


def get_logger(
    name: str = "ai_pair_programming",
    level: int = logging.INFO,
    log_file: str | None = None,
    enable_hourly_file: bool = True,
) -> OutputHandler:
    """
    Retrieve or instantiate a standardized OutputHandler.

    Args:
        name (str): Logging subsystem namespace.
        level (int): Logging severity threshold.
        log_file (str | None): Optional target file path for log entries.
        enable_hourly_file (bool): Whether to log to hourly rotating file.

    Returns:
        OutputHandler: Configured OutputHandler instance.

    """
    if name not in _LOGGERS or log_file is not None:
        _LOGGERS[name] = OutputHandler(
            name=name,
            level=level,
            log_file=log_file,
            enable_hourly_file=enable_hourly_file,
        )
    return _LOGGERS[name]
