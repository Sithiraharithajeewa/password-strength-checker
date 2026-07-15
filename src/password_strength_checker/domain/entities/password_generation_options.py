"""Domain options for secure password generation."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PasswordGenerationOptions:
    """User-selected rules for generating a secure password."""

    length: int
    include_uppercase: bool = True
    include_lowercase: bool = True
    include_numbers: bool = True
    include_symbols: bool = True
