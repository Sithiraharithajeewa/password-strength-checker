"""Secure password generation service."""

from __future__ import annotations

import secrets
import string

from password_strength_checker.domain.entities.generated_password import (
    GeneratedPassword,
)
from password_strength_checker.domain.entities.password_generation_options import (
    PasswordGenerationOptions,
)
from password_strength_checker.shared.constants import (
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH,
)
from password_strength_checker.shared.exceptions import (
    InvalidPasswordGenerationOptionsError,
)


class PasswordGenerator:
    """Generate passwords with cryptographically secure randomness."""

    UPPERCASE_CHARACTERS = string.ascii_uppercase
    LOWERCASE_CHARACTERS = string.ascii_lowercase
    NUMBER_CHARACTERS = string.digits
    SYMBOL_CHARACTERS = "!@#$%^&*()-_=+[]{};:,.?/|~"

    def generate(self, options: PasswordGenerationOptions) -> GeneratedPassword:
        """Generate a password that satisfies every selected rule."""
        selected_pools = self._get_selected_character_pools(options)
        self._validate_options(options, selected_pools)

        required_characters = [
            secrets.choice(character_pool)
            for character_pool in selected_pools
        ]
        combined_pool = "".join(selected_pools)
        remaining_length = options.length - len(required_characters)
        random_characters = [
            secrets.choice(combined_pool) for _ in range(remaining_length)
        ]

        password_characters = required_characters + random_characters
        self._secure_shuffle(password_characters)

        password = "".join(password_characters)
        return GeneratedPassword(value=password, options=options)

    def _get_selected_character_pools(
        self,
        options: PasswordGenerationOptions,
    ) -> list[str]:
        """Return character pools enabled by the generation options."""
        character_pools: list[str] = []

        if options.include_uppercase:
            character_pools.append(self.UPPERCASE_CHARACTERS)
        if options.include_lowercase:
            character_pools.append(self.LOWERCASE_CHARACTERS)
        if options.include_numbers:
            character_pools.append(self.NUMBER_CHARACTERS)
        if options.include_symbols:
            character_pools.append(self.SYMBOL_CHARACTERS)

        return character_pools

    def _validate_options(
        self,
        options: PasswordGenerationOptions,
        selected_pools: list[str],
    ) -> None:
        """Raise an exception when generation options are unsafe or impossible."""
        if not selected_pools:
            raise InvalidPasswordGenerationOptionsError(
                "At least one character type must be selected."
            )
        if options.length < MIN_PASSWORD_LENGTH:
            raise InvalidPasswordGenerationOptionsError(
                f"Password length must be at least {MIN_PASSWORD_LENGTH}."
            )
        if options.length > MAX_PASSWORD_LENGTH:
            raise InvalidPasswordGenerationOptionsError(
                f"Password length must not exceed {MAX_PASSWORD_LENGTH}."
            )
        if options.length < len(selected_pools):
            raise InvalidPasswordGenerationOptionsError(
                "Password length is too short for the selected rules."
            )

    def _secure_shuffle(self, password_characters: list[str]) -> None:
        """Shuffle characters in place using a cryptographically secure RNG."""
        secure_random = secrets.SystemRandom()
        secure_random.shuffle(password_characters)
