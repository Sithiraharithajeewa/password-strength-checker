from password_strength_checker.domain.services.feedback_generator import (
    FeedbackGenerator,
)

from tests.unit.test_password_scorer import build_scorer


def test_feedback_warns_about_common_passwords() -> None:
    scorer = build_scorer({"password"})
    generator = FeedbackGenerator()

    analysis = scorer.analyze("password")
    warnings = generator.generate_warnings(analysis)
    recommendations = generator.generate_recommendations(analysis)

    assert any("common-password" in warning for warning in warnings)
    assert any("Avoid common words" in item for item in recommendations)


def test_feedback_recommends_character_variety() -> None:
    scorer = build_scorer()
    generator = FeedbackGenerator()

    analysis = scorer.analyze("lowercaseonly")
    warnings = generator.generate_warnings(analysis)

    assert any("uppercase letters" in warning for warning in warnings)
    assert any("numbers" in warning for warning in warnings)
    assert any("symbols" in warning for warning in warnings)


def test_feedback_warns_about_all_pattern_categories() -> None:
    scorer = build_scorer()
    generator = FeedbackGenerator()

    analysis = scorer.analyze("PasswordAAA123qwerty")
    warnings = generator.generate_warnings(analysis)
    recommendations = generator.generate_recommendations(analysis)

    assert "Password contains dictionary words." in warnings
    assert "Password contains repeated character patterns." in warnings
    assert "Password contains sequential characters." in warnings
    assert "Password contains keyboard patterns." in warnings
    assert any("Avoid repeated characters" in item for item in recommendations)
    assert any("Avoid sequences" in item for item in recommendations)
    assert any("Avoid keyboard paths" in item for item in recommendations)
