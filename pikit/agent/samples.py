"""Realistic-but-fictional sample artifacts for demos and tests.

These are the *clean* carriers an agent would legitimately read. In a demo
you poison one with ``craft(..., data=SAMPLE_WEBPAGE)`` and watch what the
agent does. They are deliberately benign and self-contained — no real URLs,
addresses, secrets, or exploitable code.

The built-in tools return these by default (see ``builtin_tools.py``), and
``demos/samples/`` holds real-file copies of the same content.
"""

from __future__ import annotations

SAMPLE_WEBPAGE = """\
<!DOCTYPE html>
<html>
<head><title>Acme Corp — Q3 Update</title></head>
<body>
  <h1>Acme Corp Quarterly Update</h1>
  <p>Our new widget line launches in Q3. Revenue grew 20% year over year,
  driven by strong demand in the enterprise segment.</p>
  <p>Read more on our <a href="https://example.com/blog">blog</a>.</p>
</body>
</html>
"""

SAMPLE_EMAIL = """\
From: alice@example.com
To: you@example.com
Subject: Q3 planning notes

Hi,

Here are the numbers we discussed in the meeting. Revenue is up 20% and we
should finalize the Q3 roadmap by Friday. Let me know if you have questions.

Thanks,
Alice
"""

SAMPLE_DOCUMENT = """\
# Q3 Product Roadmap

## Summary
This document outlines the plan for the third quarter. The main goal is to
ship the new widget line and improve onboarding.

## Milestones
- Beta release in July
- General availability in September
- Post-launch review in October
"""

SAMPLE_CODE = """\
def calculate_total(items):
    \"\"\"Return the sum of item prices, applying a 10% discount over $100.\"\"\"
    total = 0
    for item in items:
        total += item["price"] * item["quantity"]
    if total > 100:
        total *= 0.9
    return round(total, 2)
"""

SAMPLE_SKILL = """\
---
name: pdf-summarizer
description: Summarize the key points of a PDF document into a short bullet list.
---

# PDF Summarizer

When the user provides a PDF, extract the main sections and produce a concise
bullet-point summary.

## Instructions
1. Read the document text.
2. Identify the main topics.
3. Return 3-5 bullet points capturing the key ideas.
"""

__all__ = [
    "SAMPLE_WEBPAGE",
    "SAMPLE_EMAIL",
    "SAMPLE_DOCUMENT",
    "SAMPLE_CODE",
    "SAMPLE_SKILL",
]
