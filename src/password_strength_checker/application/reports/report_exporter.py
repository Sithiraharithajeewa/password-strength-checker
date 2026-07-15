"""Export password analysis reports to files."""

from __future__ import annotations

from pathlib import Path

from password_strength_checker.application.dto.password_analysis_dto import (
    PasswordAnalysisDTO,
)
from password_strength_checker.application.reports.csv_report import (
    format_csv_report,
)
from password_strength_checker.application.reports.json_report import (
    format_json_report,
)
from password_strength_checker.application.reports.txt_report import (
    format_txt_report,
)


class ReportExporter:
    """Export password analysis reports in supported file formats."""

    _FORMATTERS = {
        ".txt": format_txt_report,
        ".json": format_json_report,
        ".csv": format_csv_report,
    }

    def export(self, analysis: PasswordAnalysisDTO, file_path: Path) -> None:
        """Write the analysis report to the requested file path."""
        suffix = file_path.suffix.lower()
        formatter = self._FORMATTERS.get(suffix)
        if formatter is None:
            supported_formats = ", ".join(sorted(self._FORMATTERS))
            raise ValueError(f"Unsupported report format: {supported_formats}")

        file_path.write_text(formatter(analysis), encoding="utf-8")
