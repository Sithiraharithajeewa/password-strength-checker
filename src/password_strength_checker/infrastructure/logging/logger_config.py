"""Logging configuration for the application."""

from __future__ import annotations

import logging
from pathlib import Path


def configure_logging(log_file_path: Path, level: int = logging.INFO) -> None:
    """Configure console and file logging for the application."""
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file_path, encoding="utf-8"),
        ],
    )
