"""Preconfigured scenario agents with realistic toolsets and sinks."""

from __future__ import annotations

# Importing the modules triggers their @register decorators.
from . import browser, coding, email_assistant, rag_qa  # noqa: F401

__all__ = ["email_assistant", "rag_qa", "browser", "coding"]
