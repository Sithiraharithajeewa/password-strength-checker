import string

import pytest

from password_strength_checker.domain.entities.password_generation_options import (
    PasswordGenerationOptions,
)
from password_strength_checker.domain.services.password_generator import (
    PasswordGenerator,
)
from password_strength_checker.shared.exceptions import (
    InvalidPasswordGenerationOptionsError,
)


def test_generated_password_satisfies_all_selected_rules() -> None:
    generator = PasswordGenerator()
    options = PasswordGenerationOptions(length=24)

    generated_password = generator.generate(options)

    assert len(generated_password.value) == 24
    assert any(character.isupper() for character in generated_password.value)
    assert any(character.islower() for character in generated_password.value)
    assert any(character.isdigit() for character in generated_password.value)
    assert any(
        character in PasswordGenerator.SYMBOL_CHARACTERS
        for character in generated_password.value
    )


def test_generated_password_uses_only_selected_character_types() -> None:
    generator = PasswordGenerator()
    options = PasswordGenerationOptions(
        length=16,
        include_uppercase=False,
        include_lowercase=True,
        include_numbers=True,
        include_symbols=False,
    )

    generated_password = generator.generate(options)
    allowed_characters = set(string.ascii_lowercase + string.digits)

    assert set(generated_password.value).issubset(allowed_characters)
    assert any(character.islower() for character in generated_password.value)
    assert any(character.isdigit() for character in generated_password.value)
    assert not any(character.isupper() for character in generated_password.value)


def test_generator_rejects_no_selected_character_types() -> None:
    generator = PasswordGenerator()
    options = PasswordGenerationOptions(
        length=12,
        include_uppercase=False,
        include_lowercase=False,
        include_numbers=False,
        include_symbols=False,
    )

    with pytest.raises(InvalidPasswordGenerationOptionsError):
        generator.generate(options)


def test_generator_rejects_passwords_shorter_than_policy() -> None:
    generator = PasswordGenerator()
    options = PasswordGenerationOptions(length=8)

    with pytest.raises(InvalidPasswordGenerationOptionsError):
        generator.generate(options)


@pytest.mark.parametrize(
    (
        "include_uppercase",
        "include_lowercase",
        "include_numbers",
        "include_symbols",
        "allowed_characters",
    ),
    [
        (True, False, False, False, string.ascii_uppercase),
        (False, True, False, False, string.ascii_lowercase),
        (False, False, True, False, string.digits),
        (False, False, False, True, PasswordGenerator.SYMBOL_CHARACTERS),
    ],
)
def test_single_selected_character_type_is_respected(
    include_uppercase: bool,
    include_lowercase: bool,
    include_numbers: bool,
    include_symbols: bool,
    allowed_characters: str,
) -> None:
    generator = PasswordGenerator()
    options = PasswordGenerationOptions(
        length=12,
        include_uppercase=include_uppercase,
        include_lowercase=include_lowercase,
        include_numbers=include_numbers,
        include_symbols=include_symbols,
    )

    generated_password = generator.generate(options)

    assert set(generated_password.value).issubset(set(allowed_characters))


def test_generator_rejects_passwords_longer_than_policy() -> None:
    generator = PasswordGenerator()
    options = PasswordGenerationOptions(length=129)

    with pytest.raises(InvalidPasswordGenerationOptionsError):
        generator.generate(options)


def test_generated_password_keeps_generation_options() -> None:
    generator = PasswordGenerator()
    options = PasswordGenerationOptions(
        length=18,
        include_uppercase=True,
        include_lowercase=False,
        include_numbers=True,
        include_symbols=False,
    )

    generated_password = generator.generate(options)

    assert generated_password.options == options
    assert len(generated_password.value) == options.length
