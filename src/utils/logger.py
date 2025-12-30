import logging
import sys
from pathlib import Path


def setup_logger(name: str, log_file: Path = None, level=logging.INFO):
    """Set up logger that resets log file each run."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers
    logger.handlers.clear()

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (overwrites each run)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        # 'w' mode truncates file each time
        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Usage
logger = setup_logger("BTD6Bot", Path("logs/bot.log"))
