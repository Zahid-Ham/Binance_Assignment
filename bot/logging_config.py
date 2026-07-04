import sys
from pathlib import Path
from loguru import logger

# Base directory for logs
LOGS_DIR = Path(__file__).resolve().parents[1] / "logs"


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure loguru logger with beautiful output using rich
    and daily rotating log files.
    """
    # Create logs directory if it doesn't exist
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Clear default logger handlers
    logger.remove()

    # Log format structure
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # 1. Console handler with colors
    logger.add(
        sys.stderr,
        format=log_format,
        level=log_level,
        colorize=True,
    )

    # 2. File handler with daily rotation
    log_file_path = LOGS_DIR / "trading_bot.log"
    logger.add(
        log_file_path,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
        rotation="00:00",  # Rotates every day at midnight
        retention="30 days",  # Keep logs for 30 days
        compression="zip",  # Compress older logs
    )

    logger.debug("Logging configuration initialized successfully.")
