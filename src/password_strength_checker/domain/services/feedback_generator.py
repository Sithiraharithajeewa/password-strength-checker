"""Generate user-facing security feedback."""

from password_strength_checker.domain.entities.password_analysis import (
    PasswordAnalysis,
)
from password_strength_checker.shared.constants import (
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH,
)


class FeedbackGenerator:
    """Create warnings and recommendations from password analysis."""

    def generate_warnings(self, analysis: PasswordAnalysis) -> list[str]:
        """Return security warnings for detected weaknesses."""
        warnings: list[str] = []

        if not analysis.has_minimum_length:
            warnings.append(
                f"Password is shorter than {MIN_PASSWORD_LENGTH} characters."
            )
        if not analysis.has_acceptable_length:
            warnings.append(
                f"Password is longer than {MAX_PASSWORD_LENGTH} characters."
            )
        if analysis.is_common_password:
            warnings.append("Password appears in a common-password list.")
        if analysis.has_dictionary_words:
            warnings.append("Password contains dictionary words.")
        if analysis.has_repeated_characters:
            warnings.append("Password contains repeated character patterns.")
        if analysis.has_sequential_characters:
            warnings.append("Password contains sequential characters.")
        if analysis.has_keyboard_patterns:
            warnings.append("Password contains keyboard patterns.")

        missing_categories = []
        if not analysis.has_uppercase:
            missing_categories.append("uppercase letters")
        if not analysis.has_lowercase:
            missing_categories.append("lowercase letters")
        if not analysis.has_number:
            missing_categories.append("numbers")
        if not analysis.has_symbol:
            missing_categories.append("symbols")

        if missing_categories:
            warnings.append(f"Password is missing {', '.join(missing_categories)}.")

        return warnings

    def generate_recommendations(self, analysis: PasswordAnalysis) -> list[str]:
        """Return actionable recommendations for improving strength."""
        recommendations: list[str] = []

        if not analysis.has_minimum_length:
            recommendations.append(
                f"Use at least {MIN_PASSWORD_LENGTH} characters; "
                "14 or more is better."
            )
        if analysis.is_common_password or analysis.has_dictionary_words:
            recommendations.append(
                "Avoid common words, names, slogans, and predictable substitutions."
            )
        if analysis.has_repeated_characters:
            recommendations.append(
                "Avoid repeated characters such as aaa or 111."
            )
        if analysis.has_sequential_characters:
            recommendations.append(
                "Avoid sequences such as abc, cba, 123, or 321."
            )
        if analysis.has_keyboard_patterns:
            recommendations.append("Avoid keyboard paths such as qwerty or asdf.")
        if not analysis.has_symbol:
            recommendations.append(
                "Add at least one symbol for more character variety."
            )
        if not analysis.has_number:
            recommendations.append(
                "Add numbers that are not simple dates or sequences."
            )
        if not analysis.has_uppercase or not analysis.has_lowercase:
            recommendations.append("Mix uppercase and lowercase letters.")
        if analysis.score >= 80:
            recommendations.append(
                "Password has strong characteristics; keep it unique."
            )

        return recommendations
