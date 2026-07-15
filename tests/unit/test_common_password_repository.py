from pathlib import Path

import pytest

from password_strength_checker.infrastructure.repositories import (
    file_common_password_repository as repository_module,
)
from password_strength_checker.shared.exceptions import ResourceLoadError


def test_file_common_password_repository_loads_passwords(tmp_path: Path) -> None:
    password_file = tmp_path / "common_passwords.txt"
    password_file.write_text("# comment\npassword\nAdmin123\n\n", encoding="utf-8")
    repository = repository_module.FileCommonPasswordRepository(password_file)

    assert repository.is_common_password("password") is True
    assert repository.is_common_password("admin123") is True
    assert repository.is_common_password("unique-password") is False


def test_file_common_password_repository_strips_input(tmp_path: Path) -> None:
    password_file = tmp_path / "common_passwords.txt"
    password_file.write_text("letmein\n", encoding="utf-8")
    repository = repository_module.FileCommonPasswordRepository(password_file)

    assert repository.is_common_password(" LETMEIN ") is True


def test_missing_common_password_file_can_fail_fast(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(ResourceLoadError):
        repository_module.FileCommonPasswordRepository(
            missing_file,
            fail_on_missing=True,
        )


def test_missing_common_password_file_defaults_to_empty_set(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.txt"
    repository = repository_module.FileCommonPasswordRepository(missing_file)

    assert repository.is_common_password("password") is False
