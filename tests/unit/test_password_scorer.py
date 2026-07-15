from password_strength_checker.domain.repositories.common_password_repository import (
    CommonPasswordRepository,
)
from password_strength_checker.domain.services.entropy_calculator import (
    EntropyCalculator,
)
from password_strength_checker.domain.services.password_scorer import PasswordScorer
from password_strength_checker.domain.services.pattern_detector import PatternDetector


class FakeCommonPasswordRepository(CommonPasswordRepository):
    def __init__(self, common_passwords: set[str]) -> None:
        self._common_passwords = common_passwords

    def is_common_password(self, password: str) -> bool:
        return password.lower() in self._common_passwords


def build_scorer(common_passwords: set[str] | None = None) -> PasswordScorer:
    return PasswordScorer(
        entropy_calculator=EntropyCalculator(),
        pattern_detector=PatternDetector(),
        common_password_repository=FakeCommonPasswordRepository(
            common_passwords or set()
        ),
    )


def test_common_password_is_capped_to_very_low_score() -> None:
    scorer = build_scorer({"password"})

    analysis = scorer.analyze("password")

    assert analysis.is_common_password is True
    assert analysis.score <= 15


def test_strong_password_scores_well() -> None:
    scorer = build_scorer()

    analysis = scorer.analyze("Violet-River-92!Anchor")

    assert analysis.score >= 70
    assert analysis.has_uppercase is True
    assert analysis.has_lowercase is True
    assert analysis.has_number is True
    assert analysis.has_symbol is True


def test_short_password_fails_minimum_length() -> None:
    scorer = build_scorer()

    analysis = scorer.analyze("A1!short")

    assert analysis.has_minimum_length is False
    assert analysis.score < 50


def test_validation_flags_detect_all_character_categories() -> None:
    scorer = build_scorer()

    analysis = scorer.analyze("Abcdef 12345!")

    assert analysis.has_minimum_length is True
    assert analysis.has_acceptable_length is True
    assert analysis.has_uppercase is True
    assert analysis.has_lowercase is True
    assert analysis.has_number is True
    assert analysis.has_symbol is True
    assert analysis.has_space is True


def test_validation_flags_report_missing_character_categories() -> None:
    scorer = build_scorer()

    analysis = scorer.analyze("lowercaseonly")

    assert analysis.has_uppercase is False
    assert analysis.has_lowercase is True
    assert analysis.has_number is False
    assert analysis.has_symbol is False
    assert analysis.has_space is False


def test_too_long_password_fails_maximum_length() -> None:
    scorer = build_scorer()

    analysis = scorer.analyze("A" * 129 + "a1!")

    assert analysis.has_acceptable_length is False


def test_repeated_sequential_keyboard_and_dictionary_flags() -> None:
    scorer = build_scorer()

    analysis = scorer.analyze("PasswordAAA123qwerty!")

    assert analysis.has_repeated_characters is True
    assert analysis.has_sequential_characters is True
    assert analysis.has_keyboard_patterns is True
    assert analysis.has_dictionary_words is True
    assert analysis.repeated_characters
    assert analysis.sequential_patterns
    assert analysis.keyboard_patterns
    assert "password" in analysis.dictionary_words


def test_common_password_lookup_is_case_insensitive() -> None:
    scorer = build_scorer({"password123"})

    analysis = scorer.analyze("Password123")

    assert analysis.is_common_password is True
    assert analysis.score <= 15


def test_empty_password_returns_zero_like_analysis() -> None:
    scorer = build_scorer()

    analysis = scorer.analyze("")

    assert analysis.length == 0
    assert analysis.entropy_bits == 0.0
    assert analysis.score == 0
    assert analysis.strength_level == "Very Weak"
