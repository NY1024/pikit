"""Safe, headless adapters for installed agent runtimes.

These adapters are intentionally process boundaries rather than imports of
runtime internals. They make it possible to test terminal-only deployments
without enabling chat channels, Docker, shell tools, or real delivery sinks.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from ..agent.base import Trace, TraceStep
from ..agent.hooks import DefenseHooks


class RuntimeCLIAdapter:
    """Base class for a one-shot, headless agent-runtime command.

    Subclasses implement :meth:`build_command`. The process receives a
    hardened user message and returns its captured stdout as final text unless
    a runtime-specific parser extracts a structured final response.

    No command is executed until :meth:`run` is called. The adapter never
    enables a messaging channel or delivery flag on its own.
    """

    name = "runtime_cli"

    def __init__(
        self,
        executable: str,
        *,
        system: Optional[str] = None,
        defenses: Optional[DefenseHooks] = None,
        timeout: int = 120,
        env: Optional[Dict[str, str]] = None,
    ) -> None:
        self.executable = executable
        self.system = system
        self.hooks = defenses or DefenseHooks()
        self.timeout = timeout
        self.env = dict(env or {})

    def is_available(self) -> bool:
        """Return whether the configured runtime executable is on ``PATH``."""
        return shutil.which(self.executable) is not None

    def build_command(self, user_message: str) -> list:
        """Build the non-interactive command for one agent turn."""
        raise NotImplementedError

    def parse_output(self, stdout: str) -> str:
        """Return final text from command stdout; subclasses may override."""
        return stdout.strip()

    def run(self, user_message: str, **kwargs: Any) -> Trace:
        """Run the runtime in a subprocess and translate it into a trace."""
        if not self.is_available():
            raise FileNotFoundError(
                f"{self.executable!r} was not found on PATH; install the "
                f"runtime or pass executable=..."
            )

        system = self.hooks.on_system(self.system)
        message = self.hooks.on_user(user_message)
        env = os.environ.copy()
        env.update(self.env)
        env.update({str(k): str(v) for k, v in kwargs.pop("env", {}).items()})

        completed = subprocess.run(
            self.build_command(message),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=kwargs.pop("timeout", self.timeout),
            env=env,
            check=False,
            **kwargs,
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip()
            raise RuntimeError(
                f"{self.name} exited with status {completed.returncode}: {detail}"
            )

        final_text = self.parse_output(completed.stdout)
        trace = Trace()
        if system:
            trace.add(TraceStep("system", text=system))
        trace.add(TraceStep("user", text=message))
        trace.add(TraceStep("model", text=final_text))
        trace.final_text = final_text
        return trace


class OpenClawCLIAdapter(RuntimeCLIAdapter):
    """Run one local, headless OpenClaw agent turn through its CLI.

    The adapter invokes ``openclaw agent --local --json``. It never supplies
    ``--deliver`` or a channel, so OpenClaw's messaging integrations are not
    involved. Use a dedicated OpenClaw profile/configuration that only exposes
    test fixture tools when evaluating indirect injection.
    """

    name = "openclaw"

    def __init__(
        self,
        executable: str = "openclaw",
        *,
        agent: Optional[str] = None,
        model: Optional[str] = None,
        session_key: Optional[str] = "agent:main:pikit",
        thinking: Optional[str] = None,
        state_dir: Optional[str] = None,
        config_path: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(executable, **kwargs)
        self.agent = agent
        self.model = model
        self.session_key = session_key
        self.thinking = thinking
        self.state_dir = state_dir
        self.config_path = config_path

    def build_command(self, user_message: str) -> list:
        command = [
            self.executable, "agent", "--local", "--json", "--message", user_message,
        ]
        if self.agent:
            command.extend(["--agent", self.agent])
        if self.model:
            command.extend(["--model", self.model])
        if self.session_key:
            command.extend(["--session-key", self.session_key])
        if self.thinking:
            command.extend(["--thinking", self.thinking])
        return command

    def parse_output(self, stdout: str) -> str:
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            return super().parse_output(stdout)
        return _extract_text(payload) or super().parse_output(stdout)

    def run(self, user_message: str, **kwargs: Any) -> Trace:
        """Run with optional isolated OpenClaw state/config paths.

        A configured provider is still required. The adapter does not perform
        onboarding because provider credentials and tool policy belong to the
        researcher's explicitly managed test profile.
        """
        env = dict(kwargs.pop("env", {}))
        if self.state_dir:
            env["OPENCLAW_STATE_DIR"] = self.state_dir
        if self.config_path:
            env["OPENCLAW_CONFIG_PATH"] = self.config_path
        return super().run(user_message, env=env, **kwargs)


class HermesCLIAdapter(RuntimeCLIAdapter):
    """Run one non-interactive Hermes CLI turn without messaging channels.

    ``hermes chat --query`` works directly in a terminal. By default the
    adapter adds ``--safe-mode`` to disable user customizations, skills,
    plugins, and MCP servers. Set ``safe_mode=False`` only with a dedicated
    isolated Hermes profile and an explicit tool policy.
    """

    name = "hermes"

    def __init__(
        self,
        executable: str = "hermes",
        *,
        model: Optional[str] = None,
        toolsets: Optional[Iterable[str]] = None,
        safe_mode: bool = True,
        hermes_home: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(executable, **kwargs)
        self.model = model
        self.toolsets = list(toolsets or [])
        self.safe_mode = safe_mode
        self.hermes_home = hermes_home

    def build_command(self, user_message: str) -> list:
        command = [self.executable, "chat", "--query", user_message]
        if self.safe_mode:
            command.append("--safe-mode")
        if self.model:
            command.extend(["--model", self.model])
        if self.toolsets:
            command.extend(["--toolsets", ",".join(self.toolsets)])
        return command

    def run(self, user_message: str, **kwargs: Any) -> Trace:
        # A temporary HERMES_HOME prevents ordinary test runs from reading or
        # modifying the user's persistent sessions, memory, or credentials.
        if self.hermes_home:
            return super().run(
                user_message,
                env={**kwargs.pop("env", {}), "HERMES_HOME": self.hermes_home},
                **kwargs,
            )
        with tempfile.TemporaryDirectory(prefix="pikit-hermes-") as home:
            return super().run(
                user_message,
                env={**kwargs.pop("env", {}), "HERMES_HOME": str(Path(home))},
                **kwargs,
            )


def _extract_text(value: Any) -> str:
    """Best-effort extraction across OpenClaw JSON output versions."""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("text", "output", "response", "content", "message"):
            text = _extract_text(value.get(key))
            if text:
                return text
        for key in ("result", "data"):
            text = _extract_text(value.get(key))
            if text:
                return text
    if isinstance(value, list):
        return "\n".join(filter(None, (_extract_text(item) for item in value)))
    return ""


__all__ = [
    "RuntimeCLIAdapter",
    "OpenClawCLIAdapter",
    "HermesCLIAdapter",
]
