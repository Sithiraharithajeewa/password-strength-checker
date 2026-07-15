"""Use case for analyzing password strength."""

from __future__ import annotations

from password_strength_checker.application.dto.password_analysis_dto import (
    PasswordAnalysisDTO,
)
from password_strength_checker.domain.services.feedback_generator import (
    FeedbackGenerator,
)
from password_strength_checker.domain.services.password_scorer import PasswordScorer
from password_strength_checker.shared.exceptions import InvalidPasswordInputError


class AnalyzePasswordUseCase:
    """Coordinate password analysis and return a DTO for callers."""

    def __init__(
        self,
        password_scorer: PasswordScorer,
        feedback_generator: FeedbackGenerator,
    ) -> None:
        self._password_scorer = password_scorer
        self._feedback_generator = feedback_generator

    def execute(self, password: str) -> PasswordAnalysisDTO:
        """Analyze a password and return detailed results."""
        if not isinstance(password, str):
            raise InvalidPasswordInputError("Password must be a string.")

        analysis = self._password_scorer.analyze(password)
        warnings = self._feedback_generator.generate_warnings(analysis)
        recommendations = self._feedback_generator.generate_recommendations(analysis)

        return PasswordAnalysisDTO(
            length=analysis.length,
            score=analysis.score,
            strength_level=analysis.strength_level.value,
            entropy_bits=analysis.entropy_bits,
            estimated_crack_time_seconds=analysis.estimated_crack_time_seconds,
            estimated_crack_time=analysis.estimated_crack_time,
            has_minimum_length=analysis.has_minimum_length,
            has_acceptable_length=analysis.has_acceptable_length,
            has_uppercase=analysis.has_uppercase,
            has_lowercase=analysis.has_lowercase,
            has_number=analysis.has_number,
            has_symbol=analysis.has_symbol,
            has_space=analysis.has_space,
            has_repeated_characters=analysis.has_repeated_characters,
            has_sequential_characters=analysis.has_sequential_characters,
            has_keyboard_patterns=analysis.has_keyboard_patterns,
            has_dictionary_words=analysis.has_dictionary_words,
            is_common_password=analysis.is_common_password,
            repeated_characters=analysis.repeated_characters,
            sequential_patterns=analysis.sequential_patterns,
            keyboard_patterns=analysis.keyboard_patterns,
            dictionary_words=analysis.dictionary_words,
            warnings=warnings,
            recommendations=recommendations,
        )
