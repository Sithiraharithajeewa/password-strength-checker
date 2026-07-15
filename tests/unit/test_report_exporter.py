from pathlib import Path

import pytest

from password_strength_checker.application.reports.report_exporter import (
    ReportExporter,
)
from tests.integration.test_analyze_password_use_case import (
    build_analysis_use_case,
)


@pytest.mark.parametrize("suffix", [".txt", ".json", ".csv"])
def test_report_exporter_writes_supported_formats(
    tmp_path: Path,
    suffix: str,
) -> None:
    analysis = build_analysis_use_case().execute("Violet-River-92!Anchor")
    output_path = tmp_path / f"analysis{suffix}"

    ReportExporter().export(analysis, output_path)

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8")


def test_report_exporter_rejects_unsupported_format(tmp_path: Path) -> None:
    analysis = build_analysis_use_case().execute("Violet-River-92!Anchor")

    with pytest.raises(ValueError, match="Unsupported report format"):
        ReportExporter().export(analysis, tmp_path / "analysis.pdf")
