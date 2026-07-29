"""Human-readable summaries for structured pikit experiment results."""

from __future__ import annotations

import html
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List


def load(path: str) -> List[Dict[str, Any]]:
    """Load JSON or JSONL result files produced by pikit."""
    text = Path(path).read_text(encoding="utf-8")
    if path.endswith(".jsonl"):
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    data = json.loads(text)
    return data if isinstance(data, list) else [data]


def summarize(rows: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute compact outcome and coverage statistics."""
    items = [r for r in rows if "repeat_summary" not in r.get("signals", [])]
    total = len(items)
    successes = sum(bool(r.get("success")) for r in items)
    signals = Counter(signal for r in items for signal in r.get("signals", []))
    outcomes = Counter(r.get("outcome", "not_reached") for r in items)
    by_dimension = defaultdict(lambda: {"total": 0, "success": 0})
    for row in items:
        key = " × ".join([
            row.get("agent", ""), row.get("attack", ""),
            row.get("channel", ""), row.get("defense", ""),
        ])
        by_dimension[key]["total"] += 1
        by_dimension[key]["success"] += int(bool(row.get("success")))
    return {
        "total": total,
        "successes": successes,
        "success_rate": successes / total if total else 0.0,
        "signals": dict(signals),
        "outcomes": dict(outcomes),
        "combinations": dict(by_dimension),
    }


def markdown(rows: Iterable[Dict[str, Any]]) -> str:
    """Render a Markdown experiment summary."""
    summary = summarize(rows)
    lines = [
        "# pikit experiment report", "",
        f"- Runs: **{summary['total']}**",
        f"- Successes: **{summary['successes']}**",
        f"- Success rate: **{summary['success_rate']:.1%}**", "",
        "## Signals", "",
        "| Signal | Count |", "|---|---:|",
    ]
    lines.extend(f"| `{name}` | {count} |" for name, count in sorted(summary["signals"].items()))
    lines.extend(["", "## Outcomes", "", "| Outcome | Count |", "|---|---:|"])
    lines.extend(f"| `{name}` | {count} |" for name, count in sorted(summary["outcomes"].items()))
    lines.extend(["", "## Combinations", "", "| Runtime / Agent × Attack × Channel × Defense | Success |", "|---|---:|"])
    for key, stats in sorted(summary["combinations"].items()):
        lines.append(f"| {key} | {stats['success']}/{stats['total']} |")
    return "\n".join(lines) + "\n"


def html_report(rows: Iterable[Dict[str, Any]]) -> str:
    """Render a small self-contained HTML report with expandable traces."""
    rows = list(rows)
    body = markdown(rows)
    details = []
    for row in rows:
        trace = html.escape(row.get("trace", ""))
        title = html.escape(
            f"{row.get('agent')} × {row.get('attack')} × {row.get('channel')} × {row.get('defense')}"
        )
        details.append(f"<details><summary>{title}</summary><pre>{trace}</pre></details>")
    return (
        "<!doctype html><meta charset='utf-8'><title>pikit report</title>"
        "<style>body{font-family:system-ui;max-width:1100px;margin:2rem auto;padding:0 1rem}"
        "pre{white-space:pre-wrap;background:#f5f5f5;padding:1rem}table{border-collapse:collapse}"
        "td,th{border:1px solid #ccc;padding:.35rem}</style>"
        f"<pre>{html.escape(body)}</pre><h2>Traces</h2>{''.join(details)}"
    )


__all__ = ["load", "summarize", "markdown", "html_report"]
