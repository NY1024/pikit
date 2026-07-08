"""Spreadsheet channel: hide the payload inside spreadsheet cell data.

Agents that analyse spreadsheets (Excel, Google Sheets, CSV-as-sheet)
read cell values, formulas, and comments. A payload planted in a cell
value, a cell comment, or a sheet name blends in with legitimate data
and is processed verbatim by the model.
"""

from __future__ import annotations

from ..base import Channel
from . import register


@register("spreadsheet")
class SpreadsheetChannel(Channel):
    """Embed the payload in a spreadsheet cell representation.

    Works on a plain-text spreadsheet representation (``A1: value`` lines,
    one per cell), which is what a spreadsheet-reading tool would return
    to the agent after converting a .xlsx / .gsheet to text.

    Parameters
    ----------
    method:
        * ``"cell_value"`` — appended to an existing cell value (default).
        * ``"cell_comment"`` — a cell comment (``A1 [comment]: payload``).
        * ``"sheet_name"`` — the payload becomes a sheet tab name.
    """

    def __init__(self, method: str = "cell_value") -> None:
        if method not in ("cell_value", "cell_comment", "sheet_name"):
            raise ValueError(
                "method must be 'cell_value', 'cell_comment', or 'sheet_name'"
            )
        self.method = method

    def poison(self, data: str, payload: str) -> str:
        lines = data.splitlines()
        out = []
        injected = False

        for line in lines:
            if not injected and self.method == "cell_value":
                # Append payload to the first cell value line.
                stripped = line.strip()
                if stripped and ":" in stripped:
                    ref, _, val = stripped.partition(":")
                    out.append(f"{ref}: {val} {payload}")
                    injected = True
                    continue
            out.append(line)

        if not injected:
            if self.method == "cell_value":
                out.append(f"Z99: {payload}")
            elif self.method == "cell_comment":
                one_line = " ".join(payload.splitlines())
                out.append(f"A1 [comment]: {one_line}")
            else:
                one_line = " ".join(payload.splitlines())
                out.append(f"Sheet: {one_line}")

        if self.method == "cell_comment" and not injected:
            pass  # handled above
        elif self.method == "cell_comment" and injected:
            # Also add a comment line for extra coverage.
            one_line = " ".join(payload.splitlines())
            out.append(f"A1 [comment]: {one_line}")
        elif self.method == "sheet_name" and not injected:
            pass  # handled above
        elif self.method == "sheet_name" and injected:
            one_line = " ".join(payload.splitlines())
            out.append(f"Sheet: {one_line}")

        return "\n".join(out)
