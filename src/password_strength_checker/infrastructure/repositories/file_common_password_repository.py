"""File-backed common password repository."""

from __future__ import annotations

import logging
from pathlib import Path

from password_strength_checker.domain.repositories.common_password_repository import (
    CommonPasswordRepository,
)
from password_strength_checker.shared.exceptions import ResourceLoadError

logger = logging.getLogger(__name__)


class FileCommonPasswordRepository(CommonPasswordRepository):
    """Load common passwords from a text file."""

    def __init__(self, file_path: Path, fail_on_missing: bool = False) -> None:
        self._file_path = file_path
        self._fail_on_missing = fail_on_missing
        self._passwords = self._load_passwords()

    def is_common_password(self, password: str) -> bool:
        """Return True when the normalized password is commonly used."""
        return password.strip().lower() in self._passwords

    def _load_passwords(self) -> set[str]:
        if not self._file_path.exists():
            message = f"Common password file not found: {self._file_path}"
            if self._fail_on_missing:
                raise ResourceLoadError(message)
            logger.warning(message)
            return set()

        try:
            with self._file_path.open("r", encoding="utf-8") as password_file:
                passwords = {
                    line.strip().lower()
                    for line in password_file
                    if line.strip() and not line.startswith("#")
                }
        except OSError as exc:
            message = f"Could not load common password file: {self._file_path}"
            if self._fail_on_missing:
                raise ResourceLoadError(message) from exc
            logger.exception(message)
            return set()

        logger.info("Loaded %s common password entries.", len(passwords))
        return passwords
