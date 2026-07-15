"""Shared report data preparation."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from password_strength_checker.application.dto.password_analysis_dto import (
    PasswordAnalysisDTO,
)


def build_report_data(analysis: PasswordAnalysisDTO) -> dict[str, Any]:
    """Build a password-safe dictionary for report generation."""
    return {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "security_note": "The analyzed password value is not exported.",
        "summary": {
            "length": analysis.length,
            "score": analysis.score,
            "strength_level": analysis.strength_level,
            "entropy_bits": analysis.entropy_bits,
            "estimated_crack_time": analysis.estimated_crack_time,
            "estimated_crack_time_seconds": analysis.estimated_crack_time_seconds,
        },
        "requirements": {
            "minimum_length": analysis.has_minimum_length,
            "maximum_length": analysis.has_acceptable_length,
            "uppercase": analysis.has_uppercase,
            "lowercase": analysis.has_lowercase,
            "number": analysis.has_number,
            "symbol": analysis.has_symbol,
            "space": analysis.has_space,
        },
        "findings": {
            "repeated_characters": analysis.repeated_characters,
            "sequential_patterns": analysis.sequential_patterns,
            "keyboard_patterns": analysis.keyboard_patterns,
            "dictionary_words": analysis.dictionary_words,
            "common_password": analysis.is_common_password,
        },
        "warnings": analysis.warnings,
        "recommendations": analysis.recommendations,
    }
