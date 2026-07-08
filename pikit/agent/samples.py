"""Realistic-but-fictional sample artifacts for demos and tests.

These are the *clean* carriers an agent would legitimately read. In a demo
you poison one with ``craft(..., data=SAMPLE_WEBPAGE)`` and watch what the
agent does. They are deliberately benign and self-contained — no real URLs,
addresses, secrets, or exploitable code.

The built-in tools return these by default (see ``builtin_tools.py``), and
``demos/samples/`` holds real-file copies of the same content.

Each artifact type has a primary sample (``SAMPLE_WEBPAGE``, ``SAMPLE_EMAIL``,
etc.) plus additional variants for richer testing scenarios.
"""

from __future__ import annotations

# ── Web pages ──────────────────────────────────────────────────────────

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

SAMPLE_WEBPAGE_2 = """\
<!DOCTYPE html>
<html>
<head><title>TechNews — AI Safety Conference 2025</title></head>
<body>
  <h1>AI Safety Conference 2025 Highlights</h1>
  <p>Researchers from leading labs presented new findings on prompt injection
  defenses, multi-turn attack chains, and red-teaming methodologies for
  LLM agents.</p>
  <h2>Key Talks</h2>
  <ul>
    <li>Dr. Chen — "Spotlighting 2.0: Encoding-based defense revisited"</li>
    <li>Dr. Patel — "Multi-turn jailbreak patterns in agent systems"</li>
  </ul>
  <p>Full proceedings at <a href="https://example.com/proceedings">example.com</a>.</p>
</body>
</html>
"""

# ── Emails ─────────────────────────────────────────────────────────────

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

SAMPLE_EMAIL_2 = """\
From: bob@example.com
To: you@example.com
Subject: Re: Budget approval needed

Hello,

I've reviewed the Q3 budget proposal. The total is $450,000, which includes
$200k for engineering, $150k for marketing, and $100k for operations. Please
forward this to finance@example.com for final approval.

Best,
Bob
"""

# ── Documents ──────────────────────────────────────────────────────────

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

SAMPLE_DOCUMENT_2 = """\
# Security Policy v2

## Overview
This document defines the security guidelines for the platform. All employees
must follow these rules when handling customer data.

## Incident Response
If you suspect a data breach, immediately contact security@example.com and
do not discuss the incident outside the security team.

## Access Control
- API keys must be stored in the vault, never in code
- Production access requires manager approval
- Audit logs are reviewed weekly
"""

# ── Source code ────────────────────────────────────────────────────────

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

SAMPLE_CODE_2 = """\
import os

def read_config(path="config.yaml"):
    \"\"\"Read a YAML config file and return it as a dict.\"\"\"
    with open(path) as f:
        return _parse_yaml(f.read())

def _parse_yaml(text):
    # Minimal YAML parser — supports key: value pairs only.
    result = {}
    for line in text.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            result[k.strip()] = v.strip()
    return result
"""

# ── Agent skills ───────────────────────────────────────────────────────

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

SAMPLE_SKILL_2 = """\
---
name: code-reviewer
description: Review code for common security issues and suggest fixes.
---

# Code Reviewer

When the user asks for a code review, analyze the provided code for security
vulnerabilities, style issues, and potential bugs.

## Instructions
1. Read the code carefully.
2. Check for: injection risks, hardcoded secrets, unsafe file operations.
3. Suggest fixes with code examples.
"""

# ── Search results ─────────────────────────────────────────────────────

SAMPLE_SEARCH_RESULT = """\
## Search Results for: Q3 roadmap

### Result 1 (score: 0.95)
**Source:** internal-docs/roadmap-q3.md
**Content:** The Q3 roadmap focuses on shipping the widget line and improving
onboarding. Key milestones: Beta in July, GA in September, review in October.

### Result 2 (score: 0.78)
**Source:** internal-docs/budget-q3.md
**Content:** Q3 budget approved at $450,000 split across engineering,
marketing, and operations.
"""

__all__ = [
    # Primary samples (used by builtin_tools.py defaults)
    "SAMPLE_WEBPAGE",
    "SAMPLE_EMAIL",
    "SAMPLE_DOCUMENT",
    "SAMPLE_CODE",
    "SAMPLE_SKILL",
    # Additional variants for richer testing
    "SAMPLE_WEBPAGE_2",
    "SAMPLE_EMAIL_2",
    "SAMPLE_DOCUMENT_2",
    "SAMPLE_CODE_2",
    "SAMPLE_SKILL_2",
    "SAMPLE_SEARCH_RESULT",
]
