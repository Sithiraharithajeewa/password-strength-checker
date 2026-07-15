"""Password scoring service."""

from __future__ import annotations

from password_strength_checker.domain.entities.password_analysis import (
    PasswordAnalysis,
)
from password_strength_checker.domain.enums.strength_level import StrengthLevel
from password_strength_checker.domain.repositories.common_password_repository import (
    CommonPasswordRepository,
)
from password_strength_checker.domain.services.entropy_calculator import (
    EntropyCalculator,
)
from password_strength_checker.domain.services.pattern_detector import PatternDetector
from password_strength_checker.shared.constants import (
    MAX_PASSWORD_LENGTH,
    MAX_SCORE,
    MIN_PASSWORD_LENGTH,
    MIN_SCORE,
)


class PasswordScorer:
    """Analyze password characteristics and calculate a strength score."""

    def __init__(
        self,
        entropy_calculator: EntropyCalculator,
        pattern_detector: PatternDetector,
        common_password_repository: CommonPasswordRepository,
    ) -> None:
        self._entropy_calculator = entropy_calculator
        self._pattern_detector = pattern_detector
        self._common_password_repository = common_password_repository

    def analyze(self, password: str) -> PasswordAnalysis:
        """Return a complete password analysis."""
        repeated_characters = self._pattern_detector.find_repeated_characters(
            password
        )
        sequential_patterns = self._pattern_detector.find_sequential_patterns(
            password
        )
        keyboard_patterns = self._pattern_detector.find_keyboard_patterns(password)
        dictionary_words = self._pattern_detector.find_dictionary_words(password)
        entropy_bits = self._entropy_calculator.calculate_entropy(password)
        crack_seconds = self._entropy_calculator.estimate_crack_time_seconds(
            entropy_bits
        )
        crack_time = self._entropy_calculator.format_crack_time(crack_seconds)
        is_common_password = self._common_password_repository.is_common_password(
            password
        )

        has_uppercase = any(character.isupper() for character in password)
        has_lowercase = any(character.islower() for character in password)
        has_number = any(character.isdigit() for character in password)
        has_symbol = any(
            not character.isalnum() and not character.isspace()
            for character in password
        )
        has_space = any(character.isspace() for character in password)
        has_minimum_length = len(password) >= MIN_PASSWORD_LENGTH
        has_acceptable_length = len(password) <= MAX_PASSWORD_LENGTH

        score = self._calculate_score(
            password=password,
            entropy_bits=entropy_bits,
            has_uppercase=has_uppercase,
            has_lowercase=has_lowercase,
            has_number=has_number,
            has_symbol=has_symbol,
            has_space=has_space,
            repeated_characters=repeated_characters,
            sequential_patterns=sequential_patterns,
            keyboard_patterns=keyboard_patterns,
            dictionary_words=dictionary_words,
            is_common_password=is_common_password,
        )

        return PasswordAnalysis(
            length=len(password),
            score=score,
            strength_level=StrengthLevel.from_score(score),
            entropy_bits=entropy_bits,
            estimated_crack_time_seconds=round(crack_seconds, 2),
            estimated_crack_time=crack_time,
            has_minimum_length=has_minimum_length,
            has_acceptable_length=has_acceptable_length,
            has_uppercase=has_uppercase,
            has_lowercase=has_lowercase,
            has_number=has_number,
            has_symbol=has_symbol,
            has_space=has_space,
            has_repeated_characters=bool(repeated_characters),
            has_sequential_characters=bool(sequential_patterns),
            has_keyboard_patterns=bool(keyboard_patterns),
            has_dictionary_words=bool(dictionary_words),
            is_common_password=is_common_password,
            repeated_characters=repeated_characters,
            sequential_patterns=sequential_patterns,
            keyboard_patterns=keyboard_patterns,
            dictionary_words=dictionary_words,
        )

    def _calculate_score(
        self,
        password: str,
        entropy_bits: float,
        has_uppercase: bool,
        has_lowercase: bool,
        has_number: bool,
        has_symbol: bool,
        has_space: bool,
        repeated_characters: list[str],
        sequential_patterns: list[str],
        keyboard_patterns: list[str],
        dictionary_words: list[str],
        is_common_password: bool,
    ) -> int:
        score = 0

        score += min(len(password) * 2, 30)
        score += min(int(entropy_bits * 0.45), 35)
        score += sum(
            5
            for condition in (
                has_uppercase,
                has_lowercase,
                has_number,
                has_symbol,
                has_space,
            )
            if condition
        )

        if len(password) < MIN_PASSWORD_LENGTH:
            score -= 25
        if len(password) > MAX_PASSWORD_LENGTH:
            score -= 15
        if repeated_characters:
            score -= min(15, len(repeated_characters) * 5)
        if sequential_patterns:
            score -= min(15, len(sequential_patterns) * 4)
        if keyboard_patterns:
            score -= min(20, len(keyboard_patterns) * 10)
        if dictionary_words:
            score -= min(20, len(dictionary_words) * 8)
        if is_common_password:
            score = min(score, 15)

        return max(MIN_SCORE, min(MAX_SCORE, score))
