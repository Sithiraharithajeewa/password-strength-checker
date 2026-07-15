from password_strength_checker.application.use_cases.analyze_password import (
    AnalyzePasswordUseCase,
)
from password_strength_checker.application.use_cases.generate_password import (
    GeneratePasswordUseCase,
)
from password_strength_checker.main import (
    build_analyze_password_use_case,
    build_generate_password_use_case,
)


def test_build_analyze_password_use_case_returns_working_use_case() -> None:
    use_case = build_analyze_password_use_case()

    result = use_case.execute("Violet-River-92!Anchor")

    assert isinstance(use_case, AnalyzePasswordUseCase)
    assert result.score > 0


def test_build_generate_password_use_case_returns_working_use_case() -> None:
    use_case = build_generate_password_use_case()

    result = use_case.execute(16, True, True, True, True)

    assert isinstance(use_case, GeneratePasswordUseCase)
    assert len(result.password) == 16
