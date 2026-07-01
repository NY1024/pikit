"""The provider-agnostic function-calling loop shared by tool agents."""

from __future__ import annotations

from typing import Dict, List, Optional

from ..targets import Message, Target, ToolResult
from .base import Trace, TraceStep
from .hooks import DefenseHooks
from .tools import Tool


def run_tool_loop(
    target: Target,
    user_message: str,
    tools: List[Tool],
    *,
    system: Optional[str] = None,
    hooks: Optional[DefenseHooks] = None,
    poison: Optional[Dict[str, str]] = None,
    max_steps: int = 8,
) -> Trace:
    """Drive ``target.chat`` over ``tools`` until it stops calling tools.

    Parameters
    ----------
    poison:
        Map of ``tool_name -> artifact``. When the model calls a poisoned
        tool, the loop returns the artifact as that tool's result instead of
        invoking the real function (the indirect-injection delivery point,
        and it avoids real side effects during a test).
    """
    hooks = hooks or DefenseHooks()
    poison = poison or {}
    tools_by_name = {t.name: t for t in tools}
    sinks = {t.name for t in tools if t.is_sink}

    trace = Trace()

    system = hooks.on_system(system)
    if system:
        trace.add(TraceStep("system", text=system))

    user_message = hooks.on_user(user_message)
    trace.add(TraceStep("user", text=user_message))

    messages: List[Message] = [Message("user", user_message)]
    schemas = [t.to_schema() for t in tools]

    for _ in range(max_steps):
        resp = target.chat(messages, tools=schemas, system=system)
        trace.add(TraceStep("model", text=resp.text))

        if not resp.tool_calls:
            trace.final_text = resp.text
            break

        messages.append(
            Message("assistant", resp.text, tool_calls=list(resp.tool_calls))
        )

        results = []
        for call in resp.tool_calls:
            is_sink = call.name in sinks
            trace.add(
                TraceStep(
                    "tool_call",
                    tool_name=call.name,
                    args=call.args,
                    is_sink=is_sink,
                )
            )

            is_poisoned = call.name in poison
            if is_poisoned:
                raw = poison[call.name]
            elif call.name in tools_by_name:
                raw = tools_by_name[call.name](**call.args)
            else:
                raw = f"[error: unknown tool {call.name!r}]"

            content = hooks.on_tool_result(raw, call.name)
            trace.add(
                TraceStep(
                    "tool_result",
                    tool_name=call.name,
                    content=content,
                    poisoned=is_poisoned,
                )
            )
            results.append(ToolResult(id=call.id, name=call.name, content=content))

        messages.append(Message("tool", tool_results=results))
    else:
        # Loop exhausted without a tool-free turn; record best-effort text.
        trace.final_text = trace.steps[-1].text if trace.steps else ""

    return trace
