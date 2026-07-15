"""Detection of weak password patterns."""

from __future__ import annotations

import re


class PatternDetector:
    """Detect predictable password patterns."""

    KEYBOARD_PATTERNS = (
        "qwerty",
        "asdf",
        "zxcv",
        "qaz",
        "wsx",
        "1qaz",
        "2wsx",
        "12345",
        "09876",
    )
    DICTIONARY_WORDS = frozenset(
        {
            "admin",
            "computer",
            "cyber",
            "dragon",
            "football",
            "hello",
            "iloveyou",
            "internet",
            "letmein",
            "login",
            "monkey",
            "password",
            "princess",
            "qwerty",
            "secret",
            "security",
            "shadow",
            "sunshine",
            "welcome",
        }
    )
    LEETSPEAK_TRANSLATION = str.maketrans(
        {
            "0": "o",
            "1": "l",
            "3": "e",
            "4": "a",
            "5": "s",
            "7": "t",
            "@": "a",
            "$": "s",
            "!": "i",
        }
    )

    def find_repeated_characters(self, password: str) -> list[str]:
        """Return repeated character runs of three or more characters."""
        return sorted(set(re.findall(r"(.)\1{2,}", password, flags=re.IGNORECASE)))

    def find_sequential_patterns(self, password: str) -> list[str]:
        """Return ascending or descending sequential runs of three characters."""
        normalized = password.lower()
        sequences: set[str] = set()

        for index in range(len(normalized) - 2):
            chunk = normalized[index : index + 3]
            if not chunk.isalnum():
                continue

            ordinal_values = [ord(character) for character in chunk]
            ascending = ordinal_values[1] == ordinal_values[0] + 1
            ascending = ascending and ordinal_values[2] == ordinal_values[1] + 1
            descending = ordinal_values[1] == ordinal_values[0] - 1
            descending = descending and ordinal_values[2] == ordinal_values[1] - 1

            if ascending or descending:
                sequences.add(password[index : index + 3])

        return sorted(sequences)

    def find_keyboard_patterns(self, password: str) -> list[str]:
        """Return known keyboard patterns found in the password."""
        normalized = password.lower()
        findings = {
            pattern
            for pattern in self.KEYBOARD_PATTERNS
            if pattern in normalized or pattern[::-1] in normalized
        }
        return sorted(findings)

    def find_dictionary_words(self, password: str) -> list[str]:
        """Return dictionary words or simple leetspeak variants in the password."""
        normalized = password.lower()
        deobfuscated = normalized.translate(self.LEETSPEAK_TRANSLATION)
        findings = {
            word
            for word in self.DICTIONARY_WORDS
            if word in normalized or word in deobfuscated
        }
        return sorted(findings)
