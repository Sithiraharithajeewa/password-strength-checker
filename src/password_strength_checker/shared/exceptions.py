"""Custom exceptions used by the password strength checker."""


class PasswordStrengthCheckerError(Exception):
    """Base exception for application-specific errors."""


class InvalidPasswordInputError(PasswordStrengthCheckerError):
    """Raised when a password input cannot be analyzed."""


class InvalidPasswordGenerationOptionsError(PasswordStrengthCheckerError):
    """Raised when password generation options are invalid or impossible."""


class ResourceLoadError(PasswordStrengthCheckerError):
    """Raised when an application resource cannot be loaded."""
