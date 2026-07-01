"""Built-in example tools for scenario agents.

These are deliberately simple, side-effect-free stand-ins. The *data-source*
tools (``fetch_url``, ``read_email``, ``read_file``, ``search``,
``load_skill``) return realistic clean samples by default (see
``samples.py``); in an indirect-injection test you pass a ``poison`` map so
their return value becomes the attacker's artifact instead. The *sink* tools
(``send_email``, ``post_form``, ``run_command``, ``write_file``) are marked
``is_sink=True`` so the trace highlights when the model performs an
observable, externally-visible action.
"""

from __future__ import annotations

from .samples import (
    SAMPLE_DOCUMENT,
    SAMPLE_EMAIL,
    SAMPLE_SKILL,
    SAMPLE_WEBPAGE,
)
from .tools import tool


# --- data-source tools (typical poison points) -------------------------

@tool(description="Fetch the given URL and return the page HTML as text.")
def fetch_url(url: str) -> str:
    return SAMPLE_WEBPAGE


@tool(description="Read the most recent email and return its full text.")
def read_email() -> str:
    return SAMPLE_EMAIL


@tool(description="Read a local file and return its contents.")
def read_file(path: str) -> str:
    return SAMPLE_DOCUMENT


@tool(description="Search a knowledge base and return the top document.")
def search(query: str) -> str:
    return SAMPLE_DOCUMENT


@tool(description="Load an agent skill by name and return its definition.")
def load_skill(name: str) -> str:
    return SAMPLE_SKILL


# --- sink tools (observable actions) -----------------------------------

@tool(description="Send an email to a recipient.", is_sink=True)
def send_email(to: str, body: str, subject: str = "") -> str:
    return f'{{"status":"sent","to":"{to}"}}'


@tool(description="Submit data to a web form / external endpoint.", is_sink=True)
def post_form(url: str, data: str) -> str:
    return f'{{"status":"posted","url":"{url}"}}'


@tool(description="Run a shell command and return its output.", is_sink=True)
def run_command(command: str) -> str:
    return f'{{"status":"executed","command":"{command}"}}'


@tool(description="Write content to a file at the given path.", is_sink=True)
def write_file(path: str, content: str) -> str:
    return f'{{"status":"written","path":"{path}"}}'


__all__ = [
    "fetch_url",
    "read_email",
    "read_file",
    "search",
    "load_skill",
    "send_email",
    "post_form",
    "run_command",
    "write_file",
]
