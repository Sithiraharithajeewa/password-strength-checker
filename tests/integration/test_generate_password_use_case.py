import pytest

from password_strength_checker.application.use_cases.generate_password import (
    GeneratePasswordUseCase,
)
from password_strength_checker.domain.services.password_generator import (
    PasswordGenerator,
)
from password_strength_checker.shared.exceptions import (
    InvalidPasswordGenerationOptionsError,
)


def test_generate_password_use_case_returns_dto() -> None:
    use_case = GeneratePasswordUseCase(password_generator=PasswordGenerator())

    result = use_case.execute(
        length=20,
        include_uppercase=True,
        include_lowercase=True,
        include_numbers=True,
        include_symbols=True,
    )

    assert result.length == 20
    assert len(result.password) == 20
    assert result.includes_uppercase is True
    assert result.includes_lowercase is True
    assert result.includes_numbers is True
    assert result.includes_symbols is True


def test_generate_password_use_case_respects_disabled_options() -> None:
    use_case = GeneratePasswordUseCase(password_generator=PasswordGenerator())

    result = use_case.execute(
        length=20,
        include_uppercase=False,
        include_lowercase=True,
        include_numbers=False,
        include_symbols=False,
    )

    assert result.includes_uppercase is False
    assert result.includes_lowercase is True
    assert result.includes_numbers is False
    assert result.includes_symbols is False
    assert result.password.islower()
    assert result.password.isalpha()


def test_generate_password_use_case_propagates_invalid_options() -> None:
    use_case = GeneratePasswordUseCase(password_generator=PasswordGenerator())

    with pytest.raises(InvalidPasswordGenerationOptionsError):
        use_case.execute(
            length=12,
            include_uppercase=False,
            include_lowercase=False,
            include_numbers=False,
            include_symbols=False,
        )
