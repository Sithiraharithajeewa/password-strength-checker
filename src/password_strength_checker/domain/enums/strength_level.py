"""Password strength level definitions."""

from enum import StrEnum


class StrengthLevel(StrEnum):
    """Human-readable password strength levels."""

    VERY_WEAK = "Very Weak"
    WEAK = "Weak"
    MODERATE = "Moderate"
    STRONG = "Strong"
    VERY_STRONG = "Very Strong"

    @classmethod
    def from_score(cls, score: int) -> "StrengthLevel":
        """Return a strength level for a score between 0 and 100."""
        if score < 20:
            return cls.VERY_WEAK
        if score < 40:
            return cls.WEAK
        if score < 60:
            return cls.MODERATE
        if score < 80:
            return cls.STRONG
        return cls.VERY_STRONG
