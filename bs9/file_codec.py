"""Encode/decode a single text file into/out of the .bs9 format.

The .bs9 payload is plain UTF-8 text of the form::

    <encoded body>.<coder version>.<original extension>

The original file extension is stored *inside* the payload so the decoder can
restore the exact filename even though the .bs9 file itself ends in ``.bs9``.
"""

from __future__ import annotations

import logging
import os

from .constants import BS9_SUFFIX, CODER_VERSION, VERSION
from .errors import DecodeError, EncodeError
from .files import copy_file, read_text_file, remove_file, xor_file
from .header import compute_header, insert_header, make_header, parse_header, remove_header
from .tables import Codec, default_codec

log = logging.getLogger("bs9.file_codec")


def encode_file(path: str, *, codec: Codec = default_codec) -> str:
    """Encode ``path`` (a text file) into a sibling ``.bs9`` file.

    Returns the absolute path of the new ``.bs9`` file.
    """
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        raise EncodeError(f"not a file: {path}")

    content = read_text_file(path)
    encoded = codec.encode(content)

    base, ext = os.path.splitext(path)
    payload = f"{encoded}.{CODER_VERSION}.{ext.lstrip('.')}"

    temp_path = path + ".temp"
    out_path = base + "." + BS9_SUFFIX

    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(payload)

    header = make_header(BS9_SUFFIX)
    xor_key = parse_header(header).xor_key

    log.info("Encoding %s -> %s", path, out_path)
    xor_file(temp_path, out_path, xor_key)
    insert_header(out_path, header)
    remove_file(temp_path)
    return out_path


def decode_file(path: str, *, codec: Codec = default_codec) -> str:
    """Decode a ``.bs9`` file back into its original text file.

    Returns the absolute path of the restored file.  The source ``.bs9`` file
    is left untouched; callers decide whether to delete it.
    """
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        raise DecodeError(f"not a file: {path}")

    header = compute_header(path)
    if header.file_type != BS9_SUFFIX:
        raise DecodeError("coded version too low, try a lower decoder to decode it.")
    if header.version != VERSION:
        raise DecodeError("coded file's version not supported.")

    no_header_path = path + ".noheader"
    temp_path = path + ".temp"

    copy_file(path, no_header_path)
    remove_header(no_header_path)
    xor_file(no_header_path, temp_path, header.xor_key)

    payload = read_text_file(temp_path)
    parts = payload.rsplit(".", 2)
    if len(parts) != 3:
        raise DecodeError("malformed encoded payload (missing version/extension).")

    encoded, coder_version, ext = parts
    if coder_version != CODER_VERSION:
        raise DecodeError(
            "the encoded content version is not the same as the decoder's."
        )

    content = codec.decode(encoded)

    base, _ = os.path.splitext(path)  # strip the ".bs9" suffix
    out_path = base + ("." + ext if ext else "")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    remove_file(no_header_path)
    remove_file(temp_path)
    log.info("Decoded %s -> %s", path, out_path)
    return out_path
