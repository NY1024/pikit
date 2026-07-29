"""Opt-in live smoke tests for an OpenAI-compatible DeepSeek endpoint.

Run only when explicitly requested; this module is ignored unless
``PIKIT_LIVE_TESTS=1`` is set and credentials are available.
"""

from __future__ import annotations

import os

import pytest

from pikit import get_target


pytestmark = pytest.mark.live


@pytest.mark.skipif(
    os.environ.get("PIKIT_LIVE_TESTS") != "1",
    reason="set PIKIT_LIVE_TESTS=1 to enable live API smoke tests",
)
def test_deepseek_openai_compatible_query():
    """Verify a minimal real request traverses the compatible target."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY is not configured")

    target = get_target(
        os.environ.get("PIKIT_LIVE_TARGET", "openai:deepseek-v4-flash"),
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.deepseek.com"),
        api_key=api_key,
    )
    reply = target.query("Reply with exactly: PIKIT_LIVE_OK", temperature=0)
    assert reply.strip()
