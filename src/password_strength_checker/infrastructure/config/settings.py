"""Application settings."""

from dataclasses import dataclass
from pathlib import Path

from password_strength_checker.shared.constants import (
    APP_NAME,
    APP_VERSION,
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH,
)


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings for the application."""

    app_name: str = APP_NAME
    app_version: str = APP_VERSION
    minimum_password_length: int = MIN_PASSWORD_LENGTH
    maximum_password_length: int = MAX_PASSWORD_LENGTH
    project_root: Path = Path(__file__).resolve().parents[4]

    @property
    def common_passwords_path(self) -> Path:
        """Return the common password resource path."""
        return self.project_root / "resources" / "common_passwords.txt"

    @property
    def log_file_path(self) -> Path:
        """Return the application log file path."""
        return self.project_root / "logs" / "password_strength_checker.log"
