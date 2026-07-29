"""Framework adapters for running external agents through pikit.

Adapters are optional integrations: install the matching extra only when a
framework is needed.  The core package remains dependency-free.
"""

from ..agent.adapters import AgentCallable, AgentRunResult, CallableAgentAdapter
from .recorder import TraceRecorder
from .taint import TaintRouter, ToolTaintRule

__all__ = [
    "AgentCallable",
    "AgentRunResult",
    "CallableAgentAdapter",
    "TraceRecorder",
    "TaintRouter",
    "ToolTaintRule",
]
