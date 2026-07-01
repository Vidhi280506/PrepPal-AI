"""
PrepPal AI — Structured Logging
Configured loguru logger with file + console output.
"""
import sys
from pathlib import Path
from loguru import logger


def setup_logger(log_level: str = "INFO") -> None:
    """
    Configure loguru logger with console + rotating file handlers.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR).
    """
    # Remove default handler
    logger.remove()

    # Console handler — colored, human-readable
    logger.add(
        sys.stderr,
        level=log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    # File handler — structured, rotating
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger.add(
        log_dir / "preppal.log",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        enqueue=True,  # thread-safe
    )

    logger.info(f"PrepPal AI logger initialized at level={log_level}")


# Export the configured logger
__all__ = ["logger", "setup_logger"]
