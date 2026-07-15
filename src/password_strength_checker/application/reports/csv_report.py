"""CSV report generation."""

from __future__ import annotations

import csv
from io import StringIO
from typing import Any

from password_strength_checker.application.dto.password_analysis_dto import (
    PasswordAnalysisDTO,
)
from password_strength_checker.application.reports.report_data import (
    build_report_data,
)


def format_csv_report(analysis: PasswordAnalysisDTO) -> str:
    """Return a CSV password analysis report."""
    data = build_report_data(analysis)
    output = StringIO()
    writer = csv.writer(output, lineterminator="\n")

    writer.writerow(["Section", "Field", "Value"])
    writer.writerow(["Report", "Generated At UTC", data["generated_at_utc"]])
    writer.writerow(["Report", "Security Note", data["security_note"]])
    _write_mapping(writer, "Summary", data["summary"])
    _write_mapping(writer, "Requirements", data["requirements"])
    _write_mapping(writer, "Findings", data["findings"])
    _write_list(writer, "Warnings", data["warnings"])
    _write_list(writer, "Recommendations", data["recommendations"])

    return output.getvalue()


def _write_mapping(
    writer: Any,
    section: str,
    values: dict[str, Any],
) -> None:
    """Write a dictionary section to the CSV report."""
    for field_name, value in values.items():
        writer.writerow([section, _format_field_name(field_name), _format_value(value)])


def _write_list(writer: Any, section: str, values: list[str]) -> None:
    """Write a list section to the CSV report."""
    if not values:
        writer.writerow([section, "Item", "None"])
        return

    for index, value in enumerate(values, start=1):
        writer.writerow([section, f"Item {index}", value])


def _format_field_name(field_name: str) -> str:
    """Convert an internal field name into a report label."""
    return field_name.replace("_", " ").title()


def _format_value(value: Any) -> str:
    """Convert report values to CSV-safe display text."""
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, list):
        return ", ".join(value) if value else "None"
    return str(value)
