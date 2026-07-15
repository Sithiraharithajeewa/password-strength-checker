"""DTO returned after password generation."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GeneratedPasswordDTO:
    """Application-facing result for a generated password."""

    password: str
    length: int
    includes_uppercase: bool
    includes_lowercase: bool
    includes_numbers: bool
    includes_symbols: bool
