"""Stable harness protocol used by matrix experiments."""
from __future__ import annotations
from typing import Any, Protocol
from ..agent.base import Trace

class AgentHarness(Protocol):
    """An executable agent environment that returns a pikit trace."""
    name: str
    def run(self, user_message: str, **kwargs: Any) -> Trace: ...

__all__ = ["AgentHarness"]
