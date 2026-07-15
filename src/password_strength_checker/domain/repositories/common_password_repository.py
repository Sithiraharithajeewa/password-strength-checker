"""Repository abstraction for common password lookups."""

from abc import ABC, abstractmethod


class CommonPasswordRepository(ABC):
    """Interface for checking whether a password is commonly used."""

    @abstractmethod
    def is_common_password(self, password: str) -> bool:
        """Return True when the password is present in a common-password set."""
