"""TXT report generation."""

from password_strength_checker.application.dto.password_analysis_dto import (
    PasswordAnalysisDTO,
)
from password_strength_checker.application.reports.report_data import (
    build_report_data,
)


def format_txt_report(analysis: PasswordAnalysisDTO) -> str:
    """Return a well-formatted plain text password analysis report."""
    data = build_report_data(analysis)
    summary = data["summary"]
    requirements = data["requirements"]
    findings = data["findings"]

    return "\n".join(
        [
            "Password Strength Analysis Report",
            "=" * 33,
            f"Generated at UTC: {data['generated_at_utc']}",
            f"Security note: {data['security_note']}",
            "",
            "Summary",
            "-" * 7,
            f"Length: {summary['length']}",
            f"Score: {summary['score']}/100",
            f"Strength level: {summary['strength_level']}",
            f"Entropy: {summary['entropy_bits']:.2f} bits",
            f"Estimated crack time: {summary['estimated_crack_time']}",
            "",
            "Requirements",
            "-" * 12,
            *[
                f"{name.replace('_', ' ').title()}: {_format_bool(value)}"
                for name, value in requirements.items()
            ],
            "",
            "Findings",
            "-" * 8,
            f"Common password: {_format_bool(findings['common_password'])}",
            f"Repeated characters: {_format_list(findings['repeated_characters'])}",
            f"Sequential patterns: {_format_list(findings['sequential_patterns'])}",
            f"Keyboard patterns: {_format_list(findings['keyboard_patterns'])}",
            f"Dictionary words: {_format_list(findings['dictionary_words'])}",
            "",
            "Warnings",
            "-" * 8,
            *_format_bullets(data["warnings"]),
            "",
            "Recommendations",
            "-" * 15,
            *_format_bullets(data["recommendations"]),
            "",
        ]
    )


def _format_bool(value: bool) -> str:
    """Return a human-readable status for a boolean value."""
    return "Yes" if value else "No"


def _format_list(values: list[str]) -> str:
    """Return a readable string for a list of finding values."""
    return ", ".join(values) if values else "None"


def _format_bullets(values: list[str]) -> list[str]:
    """Return bullet lines, or a placeholder when no values exist."""
    if not values:
        return ["- None"]
    return [f"- {value}" for value in values]
