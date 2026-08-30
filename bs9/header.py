"""Fixed-size plain-text header prepended to every .bs9 / .bs9pck file.

Layout (always :data:`bs9.constants.HEADER_SIZE` bytes)::

    bs9_<version>_<hex>_\x00\x00          (single-file format)
    bs9pck_<version>_<hex>                (archive format)

The ``<hex>`` value is random per file; the actual XOR key is derived from it
as ``int(hex, 16) // XOR_KEY_DIVISOR``.
"""

from __future__ import annotations

import mmap
import os
import random
import shutil
import tempfile
from dataclasses import dataclass

from .constants import (
    BS9PCK_SUFFIX,
    BS9_SUFFIX,
    HEADER_SIZE,
    VERSION,
    XOR_KEY_DIVISOR,
)
from .errors import HeaderError


@dataclass(frozen=True)
class Header:
    """Parsed header, replacing the old ``[type, version, id, code]`` list."""

    file_type: str      # "bs9" or "bs9pck"
    version: str        # e.g. "1.2.185"
    key_hex: str        # e.g. "0x2f272"
    xor_key: int        # the XOR key actually applied to the payload

    def display(self) -> str:
        """Human-readable multi-line summary (same fields as the old reader)."""
        return (
            f"fileType={self.file_type}\n"
            f"readedVersion=v{self.version}\n"
            f"convert_ID={self.key_hex}(hex)\n"
            f"convert_code={self.xor_key}"
        )


def _random_hex() -> str:
    """A six-digit decimal integer rendered as ``0x...`` (always 7 chars)."""
    return hex(random.randint(100_000, 999_999))


def make_header(file_type: str, version: str = VERSION) -> bytes:
    """Build a fresh random header for ``file_type`` (``bs9`` or ``bs9pck``)."""
    if file_type not in (BS9_SUFFIX, BS9PCK_SUFFIX):
        raise HeaderError(f"unknown file type: {file_type!r}")

    body = f"{file_type}_{version}_{_random_hex()}"
    # Single-file headers carry a trailing underscore so the parser's split
    # still yields the hex value in position 2.
    if file_type == BS9_SUFFIX:
        body += "_"

    raw = body.encode("utf-8")
    if len(raw) > HEADER_SIZE:
        raise HeaderError(
            f"header too long for version {version!r} "
            f"({len(raw)} > {HEADER_SIZE} bytes)"
        )
    return raw + b"\x00" * (HEADER_SIZE - len(raw))


def parse_header(raw: bytes) -> Header:
    """Parse raw header bytes into a :class:`Header`."""
    text = raw.rstrip(b"\x00").decode("utf-8", errors="replace")
    parts = text.split("_")
    if len(parts) < 3:
        raise HeaderError(f"malformed header: {raw!r}")
    try:
        file_type = parts[0]
        version = parts[1]
        key_hex = parts[2]
        xor_key = int(key_hex, 16) // XOR_KEY_DIVISOR
    except (ValueError, IndexError) as exc:
        raise HeaderError(f"malformed header: {raw!r}") from exc

    if file_type not in (BS9_SUFFIX, BS9PCK_SUFFIX):
        raise HeaderError(f"unsupported file type in header: {file_type!r}")
    return Header(file_type, version, key_hex, xor_key)


def read_header(path: str) -> bytes:
    """Read the leading :data:`HEADER_SIZE` bytes of ``path``."""
    with open(path, "rb") as f:
        return f.read(HEADER_SIZE)


def compute_header(path: str) -> Header:
    """Read and parse the header of ``path``."""
    return parse_header(read_header(path))


def insert_header(path: str, header: bytes) -> None:
    """Prepend ``header`` to ``path`` using an in-place mmap move.

    This avoids copying the whole file, which matters for large archives.
    """
    header = bytes(header)
    if len(header) != HEADER_SIZE:
        raise HeaderError(
            f"header must be {HEADER_SIZE} bytes, got {len(header)}"
        )

    size = os.path.getsize(path)
    with open(path, "r+b") as f:
        f.seek(0, os.SEEK_END)
        f.write(b"\x00" * HEADER_SIZE)
        f.flush()
        with mmap.mmap(f.fileno(), size + HEADER_SIZE, access=mmap.ACCESS_WRITE) as mm:
            mm.move(HEADER_SIZE, 0, size)
            mm.seek(0)
            mm.write(header)


def remove_header(path: str, header_size: int = HEADER_SIZE) -> None:
    """Strip the leading ``header_size`` bytes of ``path`` (atomic replace)."""
    directory = os.path.dirname(os.path.abspath(path))
    fd, temp_path = tempfile.mkstemp(dir=directory, suffix=".noheader")
    try:
        with os.fdopen(fd, "wb") as tmp, open(path, "rb") as src:
            src.seek(header_size)
            shutil.copyfileobj(src, tmp, length=1024 * 1024)
        os.replace(temp_path, path)
    except BaseException:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise
