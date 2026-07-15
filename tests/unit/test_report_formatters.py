import json

from password_strength_checker.application.reports.csv_report import (
    format_csv_report,
)
from password_strength_checker.application.reports.json_report import (
    format_json_report,
)
from password_strength_checker.application.reports.txt_report import (
    format_txt_report,
)
from tests.integration.test_analyze_password_use_case import (
    build_analysis_use_case,
)


def test_txt_report_is_well_formatted_and_password_safe() -> None:
    analysis = build_analysis_use_case().execute("Violet-River-92!Anchor")

    report = format_txt_report(analysis)

    assert "Password Strength Analysis Report" in report
    assert "Score:" in report
    assert "Violet-River-92!Anchor" not in report


def test_json_report_is_valid_and_password_safe() -> None:
    analysis = build_analysis_use_case().execute("Violet-River-92!Anchor")

    report = format_json_report(analysis)
    parsed_report = json.loads(report)

    assert parsed_report["summary"]["score"] == analysis.score
    assert parsed_report["security_note"]
    assert "Violet-River-92!Anchor" not in report


def test_csv_report_contains_sections_and_password_is_not_exported() -> None:
    analysis = build_analysis_use_case().execute("Violet-River-92!Anchor")

    report = format_csv_report(analysis)

    assert "Section,Field,Value" in report
    assert "Summary,Score" in report
    assert "Violet-River-92!Anchor" not in report
