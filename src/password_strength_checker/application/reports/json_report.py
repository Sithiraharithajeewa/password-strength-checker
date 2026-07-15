"""JSON report generation."""

import json

from password_strength_checker.application.dto.password_analysis_dto import (
    PasswordAnalysisDTO,
)
from password_strength_checker.application.reports.report_data import (
    build_report_data,
)


def format_json_report(analysis: PasswordAnalysisDTO) -> str:
    """Return a pretty-printed JSON password analysis report."""
    return json.dumps(build_report_data(analysis), indent=2, sort_keys=True)
