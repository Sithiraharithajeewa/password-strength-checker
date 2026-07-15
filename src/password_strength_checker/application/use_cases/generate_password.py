"""Use case for secure password generation."""

from password_strength_checker.application.dto.generated_password_dto import (
    GeneratedPasswordDTO,
)
from password_strength_checker.domain.entities.password_generation_options import (
    PasswordGenerationOptions,
)
from password_strength_checker.domain.services.password_generator import (
    PasswordGenerator,
)


class GeneratePasswordUseCase:
    """Coordinate secure password generation for application callers."""

    def __init__(self, password_generator: PasswordGenerator) -> None:
        self._password_generator = password_generator

    def execute(
        self,
        length: int,
        include_uppercase: bool,
        include_lowercase: bool,
        include_numbers: bool,
        include_symbols: bool,
    ) -> GeneratedPasswordDTO:
        """Generate a password from user-selected options."""
        options = PasswordGenerationOptions(
            length=length,
            include_uppercase=include_uppercase,
            include_lowercase=include_lowercase,
            include_numbers=include_numbers,
            include_symbols=include_symbols,
        )
        generated_password = self._password_generator.generate(options)

        return GeneratedPasswordDTO(
            password=generated_password.value,
            length=len(generated_password.value),
            includes_uppercase=include_uppercase,
            includes_lowercase=include_lowercase,
            includes_numbers=include_numbers,
            includes_symbols=include_symbols,
        )
