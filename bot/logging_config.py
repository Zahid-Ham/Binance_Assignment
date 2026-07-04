"""Logging configuration setup for the Trading Bot.

Uses Loguru to structure logging outputs to both console and rotating log files.
"""

import sys
from pathlib import Path
from typing import Any
from loguru import logger

# Automatically create logs folder
LOGS_DIR = Path(__file__).resolve().parents[1] / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Define the log file path
LOG_FILE_PATH = LOGS_DIR / "trading_bot.log"


def setup_logging(log_level: str = "DEBUG") -> None:
    """Configure loguru logger handlers.

    Configures a colorized console output and a rotating file log.

    Args:
        log_level: Minimum logging level to capture. Defaults to "DEBUG".
    """
    # Clear any default handler
    logger.remove()

    # Formats containing: Date, Time, Level, Module, Function, Line Number, Message
    console_format = (
        "<green>{time:YYYY-MM-DD}</green> <cyan>{time:HH:mm:ss.SSS}</cyan> | "
        "<level>{level: <8}</level> | "
        "<magenta>{name}</magenta>:<magenta>{function}</magenta>:<magenta>{line}</magenta> - "
        "<level>{message}</level>"
    )

    file_format = (
        "{time:YYYY-MM-DD} {time:HH:mm:ss.SSS} | "
        "{level: <8} | "
        "{name}:{function}:{line} - "
        "{message}"
    )

    # Console Logger (Standard error) with color tags
    logger.add(
        sys.stderr,
        format=console_format,
        level=log_level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    # File Logger with 5MB rotation and 14 days retention
    logger.add(
        LOG_FILE_PATH,
        format=file_format,
        level=log_level,
        rotation="5 MB",
        retention="14 days",
        compression="zip",
        encoding="utf-8",
    )


def get_logger(name: str) -> Any:
    """Return a logger bound with a specific module or component name.

    Args:
        name: Name of the module or class requesting the logger.

    Returns:
        Loguru logger bound with the component name.
    """
    return logger.bind(logger_name=name)


# Run setup_logging on module load with default level
setup_logging("DEBUG")
