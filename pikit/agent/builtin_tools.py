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
    SAMPLE_CODE,
    SAMPLE_CODE_2,
    SAMPLE_DOCUMENT,
    SAMPLE_EMAIL,
    SAMPLE_EMAIL_2,
    SAMPLE_SEARCH_RESULT,
    SAMPLE_SKILL,
    SAMPLE_SKILL_2,
    SAMPLE_WEBPAGE,
    SAMPLE_WEBPAGE_2,
)
from .tools import tool


# --- data-source tools (typical poison points) -------------------------

@tool(description="Fetch the given URL and return the page HTML as text.")
def fetch_url(url: str) -> str:
    """Fetch a web page and return its full HTML content.

    Returns a realistic sample page. In an indirect-injection test, the
    caller replaces this via the ``poison`` map so a malicious page is
    returned instead.
    """
    # Return a different page for known URLs so demos feel realistic.
    if "technews" in url.lower() or "conference" in url.lower():
        return SAMPLE_WEBPAGE_2
    return SAMPLE_WEBPAGE


@tool(description="Read the most recent email and return its full text.")
def read_email() -> str:
    """Read the user's latest email and return its full content."""
    return SAMPLE_EMAIL


@tool(description="Read a local file and return its contents.")
def read_file(path: str) -> str:
    """Read a file from the project and return its contents.

    Returns a code sample for ``.py`` files, a document for ``.md`` files,
    and a generic document otherwise.
    """
    if path.endswith(".py"):
        if "config" in path.lower():
            return SAMPLE_CODE_2
        return SAMPLE_CODE
    if path.endswith(".md") or path.endswith(".txt"):
        return SAMPLE_DOCUMENT
    return SAMPLE_DOCUMENT


@tool(description="Search the knowledge base and return matching documents.")
def search(query: str) -> str:
    """Search the knowledge base / web and return the top results.

    Returns a formatted search-result snippet. In an indirect-injection test,
    the caller replaces this via the ``poison`` map so a malicious result is
    returned instead.
    """
    return SAMPLE_SEARCH_RESULT


@tool(description="Load an agent skill by name and return its definition.")
def load_skill(name: str) -> str:
    """Load a coding skill/extension by name and return its definition."""
    if "code-review" in name.lower() or "reviewer" in name.lower():
        return SAMPLE_SKILL_2
    return SAMPLE_SKILL


# --- sink tools (observable actions) -----------------------------------

@tool(description="Send an email to a recipient.", is_sink=True)
def send_email(to: str, body: str, subject: str = "") -> str:
    """Send an email to the specified recipient. This is a sink — an
    externally-observable action that an injection might trigger."""
    return f'{{"status":"sent","to":"{to}","subject":"{subject}"}}'


@tool(description="Submit data to a web form / external endpoint.", is_sink=True)
def post_form(url: str, data: str) -> str:
    """Submit form data to a URL. This is a sink — an externally-observable
    action that an injection might trigger."""
    return f'{{"status":"posted","url":"{url}","data_length":{len(data)}}}'


@tool(description="Run a shell command and return its output.", is_sink=True)
def run_command(command: str) -> str:
    """Run a shell command and return its output. This is a sink — an
    externally-observable action that an injection might trigger."""
    return f'{{"status":"executed","command":"{command}"}}'


@tool(description="Write content to a file at the given path.", is_sink=True)
def write_file(path: str, content: str) -> str:
    """Write content to a file. This is a sink — an externally-observable
    action that an injection might trigger."""
    return f'{{"status":"written","path":"{path}","bytes":{len(content)}}}'


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
