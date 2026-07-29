"""Hermes fixture handlers: no network, shell, or real sink side effects."""

import json
import os
from pathlib import Path


def _record(event):
    path = os.environ.get("PIKIT_FIXTURE_TRACE_PATH")
    if path:
        with Path(path).open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")


def read_document(args, **_kwargs):
    ref = args.get("ref", "")
    content = os.environ.get(
        "PIKIT_FIXTURE_DOCUMENT",
        "Clean fixture document: quarterly planning is on track.",
    )
    _record({
        "type": "tool_result",
        "tool": "pikit_read_document",
        "args": {"ref": ref},
        "content": content,
        "tainted": True,
    })
    return content


def record_sink(args, **_kwargs):
    _record({
        "type": "sink_call",
        "tool": "pikit_record_sink",
        "args": {
            "action": args.get("action", ""),
            "target": args.get("target", ""),
            "content": args.get("content", ""),
        },
    })
    return "Fixture sink recorded; no external action was performed."
