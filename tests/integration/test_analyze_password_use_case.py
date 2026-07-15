import pytest

from password_strength_checker.application.use_cases.analyze_password import (
    AnalyzePasswordUseCase,
)
from password_strength_checker.domain.services.feedback_generator import (
    FeedbackGenerator,
)
from password_strength_checker.shared.exceptions import InvalidPasswordInputError

from tests.unit.test_password_scorer import build_scorer


def build_analysis_use_case() -> AnalyzePasswordUseCase:
    return AnalyzePasswordUseCase(
        password_scorer=build_scorer(),
        feedback_generator=FeedbackGenerator(),
    )


def test_analyze_password_use_case_returns_detailed_analysis() -> None:
    use_case = build_analysis_use_case()

    result = use_case.execute("Violet-River-92!Anchor")

    assert result.length == 22
    assert result.score > 0
    assert result.entropy_bits > 0
    assert result.estimated_crack_time
    assert result.has_uppercase is True
    assert result.has_lowercase is True
    assert result.has_number is True
    assert result.has_symbol is True


def test_analyze_password_use_case_rejects_non_string_input() -> None:
    use_case = build_analysis_use_case()

    with pytest.raises(InvalidPasswordInputError):
        use_case.execute(123)  # type: ignore[arg-type]


def test_analyze_password_use_case_returns_feedback() -> None:
    use_case = build_analysis_use_case()

    result = use_case.execute("password")

    assert result.warnings
    assert result.recommendations
    assert result.is_common_password is False
    assert result.has_dictionary_words is True
