"""Preconfigured scenario agents with realistic toolsets and sinks."""

from __future__ import annotations

# Importing the modules triggers their @register decorators.
from . import (  # noqa: F401
    browser, coding, email_assistant, rag_qa,
    im, calendar, finance, travel, social, file_manager,
)

__all__ = [
    "email_assistant", "rag_qa", "browser", "coding",
    "im", "calendar", "finance", "travel", "social", "file_manager",
]
