"""Tests for the CLI module."""

import subprocess
import sys


def _run_cli(*args):
    """Run pikit CLI as a subprocess and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, "-m", "pikit.cli", *args],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def test_cli_list():
    code, stdout, _ = _run_cli("list")
    assert code == 0
    assert "attacks" in stdout
    assert "defenses" in stdout
    assert "channels" in stdout


def test_cli_show_attacks():
    code, stdout, _ = _run_cli("show", "attacks")
    assert code == 0
    assert "naive" in stdout


def test_cli_show_defenses():
    code, stdout, _ = _run_cli("show", "defenses")
    assert code == 0
    assert "sandwich" in stdout or "spotlighting" in stdout


def test_cli_show_channels():
    code, stdout, _ = _run_cli("show", "channels")
    assert code == 0
    assert "webpage" in stdout


def test_cli_run_supports_offline_mock_target():
    code, stdout, stderr = _run_cli(
        "run",
        "--target", "mock",
        "--agent", "chat",
        "--attack", "naive",
        "--task", "Reply with exactly: CLI_OK",
    )
    assert code == 0, stderr
    assert "target=mock" in stdout
    assert "CLI_OK" in stdout
