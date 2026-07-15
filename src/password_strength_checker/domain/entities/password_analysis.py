"""Domain entity representing a password analysis result."""

from dataclasses import dataclass, field

from password_strength_checker.domain.enums.strength_level import StrengthLevel


@dataclass(frozen=True, slots=True)
class PasswordAnalysis:
    """Complete domain result for password analysis."""

    length: int
    score: int
    strength_level: StrengthLevel
    entropy_bits: float
    estimated_crack_time_seconds: float
    estimated_crack_time: str
    has_minimum_length: bool
    has_acceptable_length: bool
    has_uppercase: bool
    has_lowercase: bool
    has_number: bool
    has_symbol: bool
    has_space: bool
    has_repeated_characters: bool
    has_sequential_characters: bool
    has_keyboard_patterns: bool
    has_dictionary_words: bool
    is_common_password: bool
    repeated_characters: list[str] = field(default_factory=list)
    sequential_patterns: list[str] = field(default_factory=list)
    keyboard_patterns: list[str] = field(default_factory=list)
    dictionary_words: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
