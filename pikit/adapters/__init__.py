"""Framework adapters for running external agents through pikit.

Adapters are optional integrations: install the matching extra only when a
framework is needed.  The core package remains dependency-free.
"""

from ..agent.adapters import AgentCallable, AgentRunResult, CallableAgentAdapter
from .recorder import TraceRecorder
from .taint import TaintRouter, ToolTaintRule
from .runtime_cli import HermesCLIAdapter, OpenClawCLIAdapter, RuntimeCLIAdapter
from .runtime_fixtures import CHANNEL_FIXTURES, FIXTURES, RuntimeFixture, fixture_for

__all__ = [
    "AgentCallable",
    "AgentRunResult",
    "CallableAgentAdapter",
    "TraceRecorder",
    "TaintRouter",
    "ToolTaintRule",
    "RuntimeCLIAdapter",
    "OpenClawCLIAdapter",
    "HermesCLIAdapter",
    "RuntimeFixture",
    "FIXTURES",
    "CHANNEL_FIXTURES",
    "fixture_for",
]
