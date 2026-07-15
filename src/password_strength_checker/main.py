"""Backend dependency factory for the password strength checker."""

from password_strength_checker.application.use_cases.analyze_password import (
    AnalyzePasswordUseCase,
)
from password_strength_checker.application.use_cases.generate_password import (
    GeneratePasswordUseCase,
)
from password_strength_checker.domain.services.entropy_calculator import (
    EntropyCalculator,
)
from password_strength_checker.domain.services.feedback_generator import (
    FeedbackGenerator,
)
from password_strength_checker.domain.services.password_generator import (
    PasswordGenerator,
)
from password_strength_checker.domain.services.password_scorer import PasswordScorer
from password_strength_checker.domain.services.pattern_detector import PatternDetector
from password_strength_checker.infrastructure.config.settings import Settings
from password_strength_checker.infrastructure.logging.logger_config import (
    configure_logging,
)
from password_strength_checker.infrastructure.repositories import (
    file_common_password_repository as password_repository,
)


def build_analyze_password_use_case() -> AnalyzePasswordUseCase:
    """Build the password analysis use case with production dependencies."""
    settings = Settings()
    configure_logging(settings.log_file_path)

    common_password_repository = password_repository.FileCommonPasswordRepository(
        settings.common_passwords_path
    )
    password_scorer = PasswordScorer(
        entropy_calculator=EntropyCalculator(),
        pattern_detector=PatternDetector(),
        common_password_repository=common_password_repository,
    )

    return AnalyzePasswordUseCase(
        password_scorer=password_scorer,
        feedback_generator=FeedbackGenerator(),
    )


def build_generate_password_use_case() -> GeneratePasswordUseCase:
    """Build the password generation use case with production dependencies."""
    return GeneratePasswordUseCase(password_generator=PasswordGenerator())


def main() -> None:
    """Start the Tkinter desktop application."""
    from password_strength_checker.presentation.app import (
        PasswordStrengthCheckerApp,
    )

    app = PasswordStrengthCheckerApp(
        analyze_password_use_case=build_analyze_password_use_case(),
        generate_password_use_case=build_generate_password_use_case(),
    )
    app.run()


if __name__ == "__main__":
    main()
