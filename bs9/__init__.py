"""Bs9 file format library.

A small, self-contained library implementing the "bs9" text substitution
format and the "bs9pck" archive format.  The four console/GUI executables
(``console.py``, ``main.py``, ``decoder.py``, ``bs9FileInfoReader.py``) are
thin wrappers around this package.
"""

from __future__ import annotations

from .constants import (
    AUTHOR,
    BS9PCK_SUFFIX,
    BS9_SUFFIX,
    CODER_VERSION,
    DATE,
    HEADER_SIZE,
    TEXT_SUFFIXES,
    VERSION,
    XOR_KEY_DIVISOR,
)
from .errors import Bs9Error, DecodeError, EncodeError, HeaderError, PackError
from .header import Header, compute_header, insert_header, make_header, parse_header, read_header
from .file_codec import decode_file, encode_file
from .pack import pack, unpack
from .tables import Codec, TABLE_0x1A5F, TABLE_0x9910, default_codec

__version__ = VERSION

__all__ = [
    # constants
    "AUTHOR", "BS9PCK_SUFFIX", "BS9_SUFFIX", "CODER_VERSION", "DATE",
    "HEADER_SIZE", "TEXT_SUFFIXES", "VERSION", "XOR_KEY_DIVISOR",
    # errors
    "Bs9Error", "DecodeError", "EncodeError", "HeaderError", "PackError",
    # header
    "Header", "compute_header", "insert_header", "make_header",
    "parse_header", "read_header",
    # codec
    "Codec", "TABLE_0x1A5F", "TABLE_0x9910", "default_codec",
    # file codec + pack
    "decode_file", "encode_file", "pack", "unpack",
    "__version__",
]
