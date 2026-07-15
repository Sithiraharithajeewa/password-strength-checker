import pytest

from password_strength_checker.domain.enums.strength_level import StrengthLevel


@pytest.mark.parametrize(
    ("score", "expected_level"),
    [
        (0, StrengthLevel.VERY_WEAK),
        (19, StrengthLevel.VERY_WEAK),
        (20, StrengthLevel.WEAK),
        (39, StrengthLevel.WEAK),
        (40, StrengthLevel.MODERATE),
        (59, StrengthLevel.MODERATE),
        (60, StrengthLevel.STRONG),
        (79, StrengthLevel.STRONG),
        (80, StrengthLevel.VERY_STRONG),
        (100, StrengthLevel.VERY_STRONG),
    ],
)
def test_strength_level_from_score_boundaries(
    score: int,
    expected_level: StrengthLevel,
) -> None:
    assert StrengthLevel.from_score(score) == expected_level
