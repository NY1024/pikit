"""Abstract base classes for attacks, defenses, and channels.

An :class:`Attack` and a :class:`Defense` are *prompt-text transformers*:
they take a prompt string and return a new prompt string. Keeping them on
the same shape is what lets callers freely compose any attack with any
defense.

A :class:`Channel` models *indirect* injection — it hides a payload inside
an external data artifact (web page, document, email) and returns the full
prompt the target would receive after reading it. Channels are orthogonal
to attacks: word a payload with an attack, then embed it with a channel.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class Attack(ABC):
    """An injection technique that embeds an attacker task into a prompt.

    Subclasses implement :meth:`inject`. The free-form signature takes the
    full prompt (instruction + untrusted data, already assembled by the
    caller) and the attacker-controlled ``injected_task`` to smuggle in.

    Note
    ----
    An :class:`Attack` controls how the payload is *worded* (direct
    injection). To model *indirect* injection — hiding the payload inside an
    external data artifact such as a web page or document — pair an attack
    with a :class:`Channel`. The two are orthogonal and compose freely.
    """

    #: Stable identifier used by the registry and in results/logs.
    name: str = "attack"

    @abstractmethod
    def inject(self, prompt: str, injected_task: str) -> str:
        """Return ``prompt`` with ``injected_task`` smuggled in.

        Parameters
        ----------
        prompt:
            The full prompt the target would otherwise receive, typically a
            benign instruction followed by untrusted external data.
        injected_task:
            The instruction the attacker wants the model to follow instead.
        """
        raise NotImplementedError

    def __call__(self, prompt: str, injected_task: str) -> str:
        return self.inject(prompt, injected_task)

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"{type(self).__name__}(name={self.name!r})"


class Defense(ABC):
    """A prevention-style defense that hardens a prompt before querying.

    Subclasses implement :meth:`apply`. Defenses operate purely on the
    prompt text (no extra model calls), e.g. wrapping untrusted data in
    delimiters, re-stating the instruction after the data (sandwich), or
    spotlighting the data so the model can tell instructions from content.
    """

    #: Stable identifier used by the registry and in results/logs.
    name: str = "defense"

    @abstractmethod
    def apply(self, prompt: str, instruction: Optional[str] = None) -> str:
        """Return a hardened version of ``prompt``.

        Parameters
        ----------
        prompt:
            The (possibly poisoned) prompt containing untrusted data.
        instruction:
            The original benign instruction, when the caller can separate it
            from the data. Defenses that need to re-assert the task
            (sandwich, instructional) use it; others may ignore it. When
            omitted, the whole prompt is treated as untrusted data.
        """
        raise NotImplementedError

    def __call__(self, prompt: str, instruction: Optional[str] = None) -> str:
        return self.apply(prompt, instruction)

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"{type(self).__name__}(name={self.name!r})"


class Channel(ABC):
    """An *indirect* injection carrier.

    Where an :class:`Attack` controls how a payload is *worded*, a Channel
    controls *where and how* the payload is hidden — inside an external data
    artifact the model later reads (a web page, a retrieved document, an
    email). The two are orthogonal and compose freely: word a payload with an
    attack, then embed it with a channel.

    Subclasses implement :meth:`poison`, which returns the poisoned data
    artifact itself (the web page / document / email). This is what an
    attacker actually controls and what an agent's compromised tool would
    return. The concrete :meth:`embed` is a convenience that prepends an
    instruction to the poisoned artifact to form a full prompt.
    """

    #: Stable identifier used by the registry and in results/logs.
    name: str = "channel"

    @abstractmethod
    def poison(self, data: str, payload: str) -> str:
        """Hide ``payload`` inside ``data``, returning the poisoned artifact.

        Parameters
        ----------
        data:
            The clean external data (page HTML, document body, email text).
        payload:
            The injected instruction to hide. May be the raw attacker task
            or the output of an :class:`Attack` (e.g. ``attack.inject("", task)``)
            to combine wording with carrier.

        Returns
        -------
        str
            The poisoned artifact — the data with the payload hidden inside,
            **not** a full prompt. Feed this to an agent's compromised tool,
            or use :meth:`embed` to turn it into a prompt.
        """
        raise NotImplementedError

    def embed(self, instruction: str, data: str, payload: str) -> str:
        """Poison ``data`` and prepend ``instruction`` to form a full prompt.

        Convenience for the non-agent case: returns ``instruction`` followed
        by the poisoned artifact — the full prompt a target would receive.
        """
        return f"{instruction}\n{self.poison(data, payload)}"

    def __call__(self, instruction: str, data: str, payload: str) -> str:
        return self.embed(instruction, data, payload)

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"{type(self).__name__}(name={self.name!r})"
