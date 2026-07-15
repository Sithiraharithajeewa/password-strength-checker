"""Password entropy and crack-time estimation."""

from __future__ import annotations

import math

from password_strength_checker.shared.constants import DEFAULT_GUESSES_PER_SECOND


class EntropyCalculator:
    """Estimate password entropy based on detected character pools."""

    LOWERCASE_POOL_SIZE = 26
    UPPERCASE_POOL_SIZE = 26
    DIGIT_POOL_SIZE = 10
    SYMBOL_POOL_SIZE = 33
    SPACE_POOL_SIZE = 1

    def calculate_entropy(self, password: str) -> float:
        """Return estimated entropy in bits for the supplied password."""
        if not password:
            return 0.0

        pool_size = self._calculate_pool_size(password)
        if pool_size == 0:
            return 0.0

        return round(len(password) * math.log2(pool_size), 2)

    def estimate_crack_time_seconds(
        self,
        entropy_bits: float,
        guesses_per_second: int = DEFAULT_GUESSES_PER_SECOND,
    ) -> float:
        """Estimate offline brute-force crack time in seconds."""
        if entropy_bits <= 0 or guesses_per_second <= 0:
            return 0.0

        return (2**entropy_bits) / guesses_per_second

    def format_crack_time(self, seconds: float) -> str:
        """Format a crack-time estimate for display with professional formatting."""
        if seconds <= 0:
            return "Instantly"
        if seconds < 1:
            return "Less than 1 second"

        # Special handling for very large timeframes
        years = seconds / 31_536_000
        if years >= 1_000_000:
            if years >= 1_000_000_000:
                return "> 1 billion years"
            else:
                # Format as "≈ X.X million years"
                millions = years / 1_000_000
                formatted = round(millions, 1)
                return f"≈ {formatted} million years"

        intervals = [
            ("year", 31_536_000),
            ("day", 86_400),
            ("hour", 3_600),
            ("minute", 60),
            ("second", 1),
        ]

        for unit, unit_seconds in intervals:
            value = seconds / unit_seconds
            if value >= 1:
                rounded = round(value, 1) if value < 10 else round(value)
                suffix = "" if rounded == 1 else "s"
                return f"{rounded:g} {unit}{suffix}"

        return "Less than 1 second"

    def _calculate_pool_size(self, password: str) -> int:
        pool_size = 0

        if any(character.islower() for character in password):
            pool_size += self.LOWERCASE_POOL_SIZE
        if any(character.isupper() for character in password):
            pool_size += self.UPPERCASE_POOL_SIZE
        if any(character.isdigit() for character in password):
            pool_size += self.DIGIT_POOL_SIZE
        if any(character.isspace() for character in password):
            pool_size += self.SPACE_POOL_SIZE
        if any(
            not character.isalnum() and not character.isspace()
            for character in password
        ):
            pool_size += self.SYMBOL_POOL_SIZE

        return pool_size
