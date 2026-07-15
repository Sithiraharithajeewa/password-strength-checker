"""Domain entity representing a generated password."""

from dataclasses import dataclass

from password_strength_checker.domain.entities.password_generation_options import (
    PasswordGenerationOptions,
)


@dataclass(frozen=True, slots=True)
class GeneratedPassword:
    """Generated password and the rules used to create it."""

    value: str
    options: PasswordGenerationOptions
