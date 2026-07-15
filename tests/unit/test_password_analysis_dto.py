from password_strength_checker.application.dto.password_analysis_dto import (
    PasswordAnalysisDTO,
)


def build_dto(**overrides: object) -> PasswordAnalysisDTO:
    values = {
        "length": 12,
        "score": 75,
        "strength_level": "Strong",
        "entropy_bits": 72.0,
        "estimated_crack_time_seconds": 120.0,
        "estimated_crack_time": "2 minutes",
        "has_minimum_length": True,
        "has_acceptable_length": True,
        "has_uppercase": True,
        "has_lowercase": True,
        "has_number": True,
        "has_symbol": True,
        "has_space": False,
        "has_repeated_characters": False,
        "has_sequential_characters": False,
        "has_keyboard_patterns": False,
        "has_dictionary_words": False,
        "is_common_password": False,
    }
    values.update(overrides)
    return PasswordAnalysisDTO(**values)


def test_passed_basic_requirements_returns_true_when_core_rules_pass() -> None:
    dto = build_dto()

    assert dto.passed_basic_requirements is True


def test_passed_basic_requirements_returns_false_when_rule_fails() -> None:
    dto = build_dto(has_symbol=False)

    assert dto.passed_basic_requirements is False
