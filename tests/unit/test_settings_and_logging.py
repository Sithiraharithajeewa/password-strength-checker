import logging
from pathlib import Path

from password_strength_checker.infrastructure.config.settings import Settings
from password_strength_checker.infrastructure.logging.logger_config import (
    configure_logging,
)


def test_settings_builds_resource_and_log_paths(tmp_path: Path) -> None:
    settings = Settings(project_root=tmp_path)

    assert settings.common_passwords_path == tmp_path / "resources" / (
        "common_passwords.txt"
    )
    assert settings.log_file_path == tmp_path / "logs" / (
        "password_strength_checker.log"
    )


def test_configure_logging_creates_log_directory(tmp_path: Path) -> None:
    log_file_path = tmp_path / "logs" / "app.log"

    configure_logging(log_file_path, level=logging.DEBUG)

    assert log_file_path.parent.exists()
