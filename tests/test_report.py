"""Tests for JSON/JSONL experiment reporting."""

from pikit import report


def test_report_summary_and_rendering(tmp_path):
    rows = [
        {
            "agent": "openclaw",
            "attack": "combined",
            "channel": "webpage",
            "defense": "none",
            "success": True,
            "signals": ["tainted_delivered", "sink_fired"],
            "trace": "trace",
        }
    ]
    assert report.summarize(rows)["success_rate"] == 1.0
    assert "openclaw" in report.markdown(rows)
    assert "<details>" in report.html_report(rows)
