"""Exception hierarchy for the bs9 library.

Callers (CLI/GUI) should catch :class:`Bs9Error` and print its message instead
of relying on bare ``except:`` clauses as the original code did.
"""

from __future__ import annotations


class Bs9Error(Exception):
    """Base class for every error raised by the bs9 library."""


class EncodeError(Bs9Error):
    """Raised when a file/text cannot be encoded."""


class DecodeError(Bs9Error):
    """Raised when a file/text cannot be decoded."""


class PackError(Bs9Error):
    """Raised when packing or unpacking a folder fails."""


class HeaderError(Bs9Error):
    """Raised when a file header is malformed or unsupported."""
