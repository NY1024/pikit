"""Agent base class and the execution :class:`Trace`.

``run()`` returns a :class:`Trace` rather than a bare string. The trace is
the artifact a human reads to judge — manually — whether an injection
succeeded: it shows every model turn, tool call, and tool result, and
highlights when a *sink* fired or a step carried *poisoned* data. The
library deliberately renders no verdict (no evaluator/scoring); it makes the
signals easy to see and offers structured accessors so you can write your
own one-line assertion.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional

from ..targets import Target
from .hooks import DefenseHooks


@dataclass
class TraceStep:
    """One step in an agent run."""

    kind: str  #: "system" | "user" | "model" | "tool_call" | "tool_result"
    text: str = ""
    tool_name: Optional[str] = None
    args: Optional[dict] = None
    content: Optional[str] = None
    poisoned: bool = False  #: tool_result whose data was the injected artifact
    is_sink: bool = False  #: tool_call to a sink tool (observable action)


@dataclass
class Trace:
    """An ordered record of an agent run, for human inspection."""

    steps: List[TraceStep] = field(default_factory=list)
    final_text: str = ""

    def add(self, step: TraceStep) -> None:
        self.steps.append(step)

    @property
    def sink_calls(self) -> List[TraceStep]:
        """Tool-call steps that hit a sink (observable action)."""
        return [s for s in self.steps if s.kind == "tool_call" and s.is_sink]

    @property
    def poisoned_steps(self) -> List[TraceStep]:
        """Steps whose data was the injected artifact."""
        return [s for s in self.steps if s.poisoned]

    def __str__(self) -> str:
        lines = []
        for s in self.steps:
            if s.kind == "system":
                lines.append(f">>> system: {s.text}")
            elif s.kind == "user":
                lines.append(f">>> user:   {s.text}")
            elif s.kind == "model":
                lines.append(f">>> model:  {s.text}")
            elif s.kind == "tool_call":
                args = s.args or {}
                marker = "   <-- SINK FIRED" if s.is_sink else ""
                lines.append(f">>> tool_call {s.tool_name}({_fmt_args(args)}){marker}")
            elif s.kind == "tool_result":
                tag = " [poisoned]" if s.poisoned else ""
                lines.append(f"<<< tool_result {s.tool_name}{tag}: {s.content}")
        return "\n".join(lines)


def _fmt_args(args: dict) -> str:
    return ", ".join(f"{k}={v!r}" for k, v in args.items())


class Agent(ABC):
    """Base class for agents under test.

    Parameters
    ----------
    target:
        The model backend (:class:`~pikit.targets.Target`).
    system:
        Optional system prompt.
    defenses:
        Optional :class:`DefenseHooks` applied at the three insertion points.
    """

    name: str = "agent"

    def __init__(
        self,
        target: Target,
        *,
        system: Optional[str] = None,
        defenses: Optional[DefenseHooks] = None,
    ) -> None:
        self.target = target
        self.system = system
        self.hooks = defenses or DefenseHooks()

    @abstractmethod
    def run(self, user_message: str, **kwargs) -> Trace:
        """Run the agent on ``user_message`` and return the :class:`Trace`."""
        raise NotImplementedError

    def __call__(self, user_message: str, **kwargs) -> Trace:
        return self.run(user_message, **kwargs)

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"{type(self).__name__}(name={self.name!r})"
