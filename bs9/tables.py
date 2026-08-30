"""Character tables and the text codec.

The "encryption" for a single text file is a substitution cipher: every
character present in the active table is replaced by its two-digit row/column
coordinate (``row*10 + col``, printed as two digits).  Any other character
(e.g. CJK text) is kept verbatim and followed by a single space so that the
decoder can tell it apart from a real coordinate.

A :class:`Codec` pre-builds both lookup directions once, replacing the
original ``Data`` class that scanned the table linearly for every character.
"""

from __future__ import annotations

from typing import Final

# Reference tables.  Only TABLE_0x9910 is active in this build (see
# bs9.constants.CODER_VERSION); the other is kept for older files/tools.
TABLE_0x1A5F: Final[list[list[str | None]]] = [
    ["3", "T", "s", "\n", ")", "N", "+", "o", "]", "x"],
    ["/", "w", "v", "S", ";", "&", "U", "2", "n", "y"],
    ["9", "t", "H", "u", "g", "f", "p", "I", "=", "m"],
    ["$", "R", ":", "h", "e", "E", None, "r", "l", "P"],
    [">", "_", "i", "G", "z", "d", "!", "V", None, "O"],
    ["8", "M", "-", "j", "Q", "c", "k", "F", "q", "?"],
    ["#", "6", "W", " ", "B", ".", "b", "`", "X", "}"],
    [",", "1", "A", None, "Y", "(", "4", "C", "~", "J"],
    ["[", "L", "*", "a", "5", "D", "|", "<", "0", "'"],
    ["\\", "%", "{", "K", "^", "\"", "7", "@", "Z", None],
]

TABLE_0x9910: Final[list[list[str | None]]] = [
    ["3", "T", "s", "\n", ")", "N", "+", "o", "]", "x"],
    ["/", "w", "v", "?", ";", "&", "U", "2", "n", "y"],
    ["9", "t", "H", "u", "g", "f", "p", "I", "=", "m"],
    ["$", "R", "G", "h", "e", "E", "\u201d", "r", "l", "P"],
    [">", "_", "i", ":", "z", "b", "!", "V", "\u201c", "O"],
    ["8", "M", "-", "j", "Q", "c", "k", "F", "q", "S"],
    ["#", "6", "W", " ", "B", ".", "d", "`", "X", "}"],
    [",", "1", "A", "\u3002", "Y", "(", "4", "C", "~", "J"],
    ["[", "L", "*", "a", "5", "D", "|", "<", "0", "'"],
    ["\\", "%", "{", "K", "^", "\"", "7", "@", "Z", "\uff0c"],
]


class Codec:
    """Bidirectional mapping between characters and two-digit coordinates."""

    def __init__(self, table: list[list[str | None]]) -> None:
        self.table: list[list[str | None]] = table
        # character -> "rc"
        self._forward: dict[str, str] = {
            ch: f"{row}{col}"
            for row, cells in enumerate(table)
            for col, ch in enumerate(cells)
            if ch is not None
        }
        # "rc" -> character (only for cells that actually hold a character)
        self._reverse: dict[str, str] = {
            code: ch for ch, code in self._forward.items()
        }

    def encode(self, text: str) -> str:
        """Encode ``text`` into a bs9 string.

        Known characters become two-digit coordinates; unknown characters are
        kept and followed by a space (the decoder's fallback marker).
        """
        return "".join(self._forward.get(ch, ch + " ") for ch in text)

    def decode(self, text: str) -> str:
        """Decode a bs9 string produced by :meth:`encode`.

        This mirrors the original behaviour exactly for well-formed input and
        degrades gracefully for malformed input instead of raising.
        """
        out: list[str] = []
        for i in range(0, len(text), 2):
            code = text[i:i + 2]
            if len(code) == 2 and code[1] == " ":
                # Fallback marker: the character is stored verbatim.
                out.append(code[0])
            elif len(code) == 2 and code.isdigit():
                out.append(self._reverse.get(code, code[0]))
            else:
                # Odd-length tail / malformed code: keep the first character.
                out.append(code[0] if code else "")
        return "".join(out)

    def show_data(self) -> None:
        """Print the table in colour (the ``show data`` debug view)."""
        from rich import print as rprint

        for row in self.table:
            for ch in row:
                if ch == "\n":
                    rprint("[bold purple]\\n[/bold purple]", end=" ")
                elif ch is None:
                    rprint(" ", end=" ")
                elif "a" <= ch <= "z" or "A" <= ch <= "Z":
                    rprint(f"[bold red]{ch}[/bold red]", end=" ")
                elif ch.isdigit():
                    rprint(f"[bold blue]{ch}[/bold blue]", end=" ")
                elif ch == "\\":
                    rprint("[bold green]\\", end=" ")
                else:
                    rprint(f"[bold green]{ch}[/bold green]", end=" ")
            rprint()


# The codec used by this build.
default_codec: Codec = Codec(TABLE_0x9910)
