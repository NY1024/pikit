"""Calendar-event channel: hide the payload inside a calendar invite.

Scheduling agents that read .ics files or calendar APIs process event
metadata — title, description, location, attendee notes. A payload
planted in one of these fields is ingested verbatim when the agent
summarises, triages, or acts on the event.
"""

from __future__ import annotations

from ..base import Channel
from . import register


@register("calendar_event")
class CalendarEventChannel(Channel):
    """Embed the payload in a calendar event field.

    Works on a plain-text calendar event representation (field ``key:
    value`` lines), which is what an agent's calendar tool would return
    after parsing an .ics file or calling a calendar API.

    Parameters
    ----------
    field:
        * ``"title"`` — the event ``Title`` (default).
        * ``"description"`` — the event ``Description``.
        * ``"location"`` — the event ``Location``.
        * ``"attendee_note"`` — an attendee ``Note`` field.
    """

    _FIELDS = ("title", "description", "location", "attendee_note")

    _FIELD_MAP = {
        "title": "Title",
        "description": "Description",
        "location": "Location",
        "attendee_note": "Note",
    }

    def __init__(self, field: str = "title") -> None:
        if field not in self._FIELDS:
            raise ValueError(
                "field must be 'title', 'description', 'location', or 'attendee_note'"
            )
        self.field = field

    def poison(self, data: str, payload: str) -> str:
        field_name = self._FIELD_MAP[self.field]
        lines = data.splitlines()
        injected = False
        out = []
        for line in lines:
            if not injected and line.strip().startswith(f"{field_name}:"):
                if self.field == "title":
                    out.append(f"{field_name}: {payload}")
                else:
                    out.append(f"{line} {payload}")
                injected = True
            else:
                out.append(line)
        if not injected:
            out.append(f"{field_name}: {payload}")
        return "\n".join(out)
