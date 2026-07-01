"""``craft()`` — the single entry point for building attack content.

It unifies the two delivery paths so the rest of the toolkit (and the user)
deals with one object:

* **direct** — the worded payload is the *user message* sent to the agent.
* **indirect** — the worded payload is hidden in a data artifact (via a
  channel); that poisoned artifact is what a compromised tool returns.

In both cases :attr:`CraftResult.delivery` is the single field the agent
consumes — as the user message (direct) or as a ``poison`` map value
(indirect).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from . import attacks, channels


@dataclass
class CraftResult:
    """The product of :func:`craft`.

    Attributes
    ----------
    mode:
        ``"direct"`` or ``"indirect"``.
    payload:
        The worded attacker instruction (the attack's output).
    delivery:
        What actually gets injected — the user message (direct) or the
        poisoned artifact (indirect).
    instruction, attack, channel:
        Reference metadata about how it was built.
    """

    mode: str
    payload: str
    delivery: str
    instruction: Optional[str] = None
    attack: Optional[str] = None
    channel: Optional[str] = None

    def __str__(self) -> str:
        return self.delivery


def craft(
    task: str,
    *,
    attack: str = "naive",
    attack_kwargs: Optional[dict] = None,
    channel: Optional[str] = None,
    channel_kwargs: Optional[dict] = None,
    data: Optional[str] = None,
    instruction: Optional[str] = None,
) -> CraftResult:
    """Build attack content for direct or indirect injection.

    Parameters
    ----------
    task:
        The instruction the attacker wants the model to follow.
    attack:
        Registry key of the wording technique (see ``pikit.attacks``).
    attack_kwargs:
        Constructor kwargs for the attack.
    channel:
        Registry key of the carrier (see ``pikit.channels``). When ``None``
        the result is *direct*; when set the result is *indirect*.
    channel_kwargs:
        Constructor kwargs for the channel.
    data:
        The clean artifact (page HTML, document, email body) to poison.
        Required for indirect injection.
    instruction:
        The benign user request. For **direct** injection, when provided it
        is prepended so ``delivery`` is the realistic *benign + payload*
        message the agent receives (e.g. "Search the weather. Ignore all
        previous instructions. Instead, ..."); omit it to get the payload
        alone. For **indirect** injection it is kept for reference (the
        carrier hides only the payload, as in a real artifact).

    Returns
    -------
    CraftResult

    Examples
    --------
    >>> craft("Print HACKED", attack="context_ignoring").mode
    'direct'
    >>> r = craft("Print HACKED", attack="naive",
    ...           instruction="Summarize this article.")
    >>> r.delivery.startswith("Summarize this article.")
    True
    >>> craft("Print HACKED", channel="webpage",
    ...       data="<html><body>hi</body></html>").mode
    'indirect'
    """
    if channel is None:
        # Direct: prepend the benign request when given, so `delivery` is the
        # realistic message the agent receives.
        base = instruction or ""
        worded = attacks.get(attack)(**(attack_kwargs or {})).inject(base, task)
        return CraftResult(
            mode="direct",
            payload=attacks.get(attack)(**(attack_kwargs or {})).inject("", task),
            delivery=worded,
            instruction=instruction,
            attack=attack,
        )

    if data is None:
        raise ValueError("indirect injection (channel set) requires `data`")

    # Indirect: the carrier hides only the payload (as in a real artifact).
    worded = attacks.get(attack)(**(attack_kwargs or {})).inject("", task)
    artifact = channels.get(channel)(**(channel_kwargs or {})).poison(data, worded)
    return CraftResult(
        mode="indirect",
        payload=worded,
        delivery=artifact,
        instruction=instruction,
        attack=attack,
        channel=channel,
    )
