"""Setup and diagnostics for isolated OpenClaw and Hermes experiment profiles."""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict

from .runtime_assets import fixture_path


def doctor(runtime: str, *, executable: str | None = None, home: str | None = None) -> Dict[str, Any]:
    """Inspect whether a runtime is ready for safe pikit fixture experiments."""
    runtime = runtime.lower()
    if runtime not in {"openclaw", "hermes"}:
        raise ValueError("runtime must be 'openclaw' or 'hermes'")
    executable = executable or runtime
    report: Dict[str, Any] = {
        "runtime": runtime,
        "executable": executable,
        "executable_found": bool(shutil.which(executable)),
        "fixture_path": fixture_path(runtime),
        "fixture_present": Path(fixture_path(runtime)).is_dir(),
        "profile": home or "",
    }
    if runtime == "openclaw":
        state = Path(home) if home else None
        report["config_present"] = bool(state and (state / "openclaw.json").is_file())
        report["fixture_hint"] = (
            "Run `npm install && npm run plugin:build` in the fixture directory, "
            "then install/link it in this isolated OpenClaw state."
        )
    else:
        state = Path(home) if home else None
        report["config_present"] = bool(state and (state / "config.yaml").is_file())
        report["fixture_plugin_present"] = bool(
            state and (state / "plugins" / "pikit_fixture" / "plugin.yaml").is_file()
        )
        report["fixture_hint"] = (
            "The fixture plugin is copied by `pikit runtime init hermes`; "
            "run with `safe_mode=false` and `toolsets=['pikit_fixture']`."
        )
    report["ready"] = bool(
        report["executable_found"] and report["fixture_present"] and report["config_present"]
    )
    return report


def init(runtime: str, directory: str) -> Dict[str, str]:
    """Create an isolated, fixture-only runtime profile skeleton.

    The command never writes provider credentials.  Operators configure model
    access separately through environment variables or the runtime's own
    onboarding flow.
    """
    runtime = runtime.lower()
    root = Path(directory).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    if runtime == "hermes":
        plugin_dest = root / "plugins" / "pikit_fixture"
        if not plugin_dest.exists():
            shutil.copytree(fixture_path("hermes"), plugin_dest)
        config = root / "config.yaml"
        if not config.exists():
            config.write_text(
                "plugins:\n  enabled:\n    - pikit_fixture\n",
                encoding="utf-8",
            )
        return {
            "runtime": runtime,
            "profile": str(root),
            "config": str(config),
            "fixture": str(plugin_dest),
        }
    if runtime == "openclaw":
        fixture_dest = root / "pikit-openclaw-fixture"
        if not fixture_dest.exists():
            shutil.copytree(fixture_path("openclaw"), fixture_dest)
        config = root / "openclaw.json"
        if not config.exists():
            config.write_text(
                json.dumps(
                    {
                        "tools": {
                            "profile": "minimal",
                            "alsoAllow": [
                                "pikit_read_document", "pikit_fetch_url",
                                "pikit_read_email", "pikit_search_knowledge",
                                "pikit_load_skill", "pikit_record_sink",
                            ],
                            "deny": ["exec", "browser", "message", "write", "edit"],
                        }
                    },
                    indent=2,
                ) + "\n",
                encoding="utf-8",
            )
        return {
            "runtime": runtime,
            "profile": str(root),
            "config": str(config),
            "fixture": str(fixture_dest),
        }
    raise ValueError("runtime must be 'openclaw' or 'hermes'")


__all__ = ["doctor", "init"]
