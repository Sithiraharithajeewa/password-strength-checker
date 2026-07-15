from password_strength_checker.domain.services.entropy_calculator import (
    EntropyCalculator,
)


def test_empty_password_has_zero_entropy() -> None:
    calculator = EntropyCalculator()

    assert calculator.calculate_entropy("") == 0.0


def test_mixed_password_has_higher_entropy_than_lowercase_only() -> None:
    calculator = EntropyCalculator()

    lowercase_entropy = calculator.calculate_entropy("correcthorsebattery")
    mixed_entropy = calculator.calculate_entropy("CorrectHorseBattery42!")

    assert mixed_entropy > lowercase_entropy


def test_crack_time_is_formatted() -> None:
    calculator = EntropyCalculator()

    seconds = calculator.estimate_crack_time_seconds(40)

    assert seconds > 0
    assert calculator.format_crack_time(seconds)


def test_symbol_and_space_entropy_uses_larger_pool() -> None:
    calculator = EntropyCalculator()

    plain_entropy = calculator.calculate_entropy("Password1234")
    symbol_space_entropy = calculator.calculate_entropy("Password 1234!")

    assert symbol_space_entropy > plain_entropy


def test_invalid_crack_time_inputs_return_zero() -> None:
    calculator = EntropyCalculator()

    assert calculator.estimate_crack_time_seconds(0) == 0.0
    assert calculator.estimate_crack_time_seconds(10, guesses_per_second=0) == 0.0


def test_crack_time_formatter_covers_ranges() -> None:
    calculator = EntropyCalculator()

    assert calculator.format_crack_time(0) == "Instantly"
    assert calculator.format_crack_time(0.5) == "Less than 1 second"
    assert calculator.format_crack_time(90) == "1.5 minutes"
    assert calculator.format_crack_time(3_600) == "1 hour"
    assert calculator.format_crack_time(31_536_000) == "1 year"
    # Test million years formatting
    assert "million years" in calculator.format_crack_time(31_536_000 * 1_000_001)
    # Test billion years formatting
    assert calculator.format_crack_time(31_536_000 * 2_000_000_000) == "> 1 billion years"
