"""PDF-metadata channel: hide the payload inside PDF metadata fields.

When a model reads a PDF — via text extraction, a retrieval pipeline, or
a summarisation tool — the document's metadata (Title, Author, Subject,
Keywords) is often included in the text stream. A payload planted in a
metadata field is invisible in the rendered page content yet present in
what the model processes.
"""

from __future__ import annotations

from ..base import Channel
from . import register


@register("pdf_metadata")
class PDFMetadataChannel(Channel):
    """Embed the payload in a PDF metadata field.

    The channel works on a plain-text representation of PDF metadata
    (``key: value`` lines, one per field). When the raw PDF bytes are not
    available — which is the common case in simulation — this text form
    is what the extraction pipeline would hand to the model.

    Parameters
    ----------
    field:
        The metadata field to inject into:
        * ``"title"`` — the ``Title`` field.
        * ``"author"`` — the ``Author`` field.
        * ``"subject"`` — the ``Subject`` field.
        * ``"keywords"`` — the ``Keywords`` field.
        * ``"custom"`` — a custom ``X-Comment`` field.
    """

    _FIELD_MAP = {
        "title": "Title",
        "author": "Author",
        "subject": "Subject",
        "keywords": "Keywords",
        "custom": "X-Comment",
    }

    def __init__(self, field: str = "title") -> None:
        if field not in self._FIELD_MAP:
            raise ValueError(
                "field must be 'title', 'author', 'subject', 'keywords', or 'custom'"
            )
        self.field = field

    def poison(self, data: str, payload: str) -> str:
        field_name = self._FIELD_MAP[self.field]
        lines = data.splitlines()
        injected = False
        out = []
        for line in lines:
            if not injected and line.strip().startswith(f"{field_name}:"):
                out.append(f"{field_name}: {payload}")
                injected = True
            else:
                out.append(line)
        if not injected:
            out.append(f"{field_name}: {payload}")
        return "\n".join(out)
