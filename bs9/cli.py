"""argparse-based command-line interface.

Replaces the hand-rolled ``if command == "..."`` dispatcher in the original
``console.py`` with a proper subcommand/flag parser.
"""

from __future__ import annotations

import argparse
import logging
import os
from typing import Callable

from .constants import BS9PCK_SUFFIX, BS9_SUFFIX, TEXT_SUFFIXES, VERSION
from .errors import Bs9Error
from .file_codec import decode_file, encode_file
from .header import compute_header
from .pack import pack, unpack
from .ui import banner

log = logging.getLogger("bs9.cli")


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"bs9_code_{VERSION}_csl.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def _normalize(path: str) -> str:
    return path.replace(os.sep, "/")


def _require_file(path: str) -> str:
    path = _normalize(path)
    if not os.path.isfile(path):
        raise Bs9Error(f"target file not allowed: {path!r}")
    return path


def _check_suffix(path: str, allowed: tuple[str, ...]) -> None:
    if path.rsplit(".", 1)[-1] not in allowed:
        raise Bs9Error(f"target file not allowed: {path!r}")


def _log_header(path: str) -> None:
    header = compute_header(path)
    log.info("fileType=%s", header.file_type)
    log.info("readedVersion=%s", header.version)
    log.info("convert_ID=%s(hex)", header.key_hex)
    log.info("convert_code=%s", header.xor_key)


def _cmd_encode(args: argparse.Namespace) -> None:
    path = _require_file(args.file)
    _check_suffix(path, TEXT_SUFFIXES)
    log.info("ENCODE COMMAND File: %s, encoding...", path)
    new_path = encode_file(path)
    _log_header(new_path)
    log.info("Encode Completed")


def _cmd_decode(args: argparse.Namespace) -> None:
    path = _require_file(args.file)
    _check_suffix(path, (BS9_SUFFIX,))
    log.info("DECODE COMMAND File: %s, decoding...", path)
    _log_header(path)
    decode_file(path)
    if not args.keep:
        os.remove(path)
    log.info("Decode Completed")


def _cmd_pack(args: argparse.Namespace) -> None:
    path = _normalize(args.folder)
    if not os.path.isdir(path):
        raise Bs9Error(f"target path not allowed: {path!r}")
    log.info("PACK COMMAND File: %s, packing...", path)
    website = (
        os.path.isfile(path + "/index.html") or os.path.isfile(path + "/index.htm")
    )
    log.info("It's a website folder" if website else "It's a normal folder")
    new_path = pack(path, website=website, remove_source=not args.keep)
    _log_header(new_path)
    log.info("Pack Completed")


def _cmd_unpack(args: argparse.Namespace) -> None:
    path = _require_file(args.file)
    _check_suffix(path, (BS9PCK_SUFFIX,))
    log.info("UNPACK COMMAND File: %s, unpacking...", path)
    _log_header(path)
    unpack(path, remove_source=not args.keep)
    log.info("Unpack Completed")


def _cmd_info(args: argparse.Namespace) -> None:
    path = _require_file(args.file)
    print(compute_header(path).display())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bs9",
        description=f"Bs9 Encoder/Decoder v{VERSION}",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"Version: {VERSION}"
    )

    sub = parser.add_subparsers(dest="command", required=True, metavar="<command>")

    p = sub.add_parser("encode", help="encode a text file into a .bs9 file")
    p.add_argument("file", help="text file to encode")
    p.set_defaults(func=_cmd_encode)

    p = sub.add_parser("decode", help="decode a .bs9 file")
    p.add_argument("file", help=".bs9 file to decode")
    p.add_argument("--keep", action="store_true",
                   help="keep the source .bs9 file (default: delete it)")
    p.set_defaults(func=_cmd_decode)

    p = sub.add_parser("pack", help="pack a folder into a .bs9pck archive")
    p.add_argument("folder", help="folder to pack")
    p.add_argument("--keep", action="store_true",
                   help="keep the source folder (default: delete it)")
    p.set_defaults(func=_cmd_pack)

    p = sub.add_parser("unpack", help="unpack a .bs9pck archive")
    p.add_argument("file", help=".bs9pck file to unpack")
    p.add_argument("--keep", action="store_true",
                   help="keep the source .bs9pck file (default: delete it)")
    p.set_defaults(func=_cmd_unpack)

    p = sub.add_parser("info", help="show the header info of a .bs9/.bs9pck file")
    p.add_argument("file", help="file to inspect")
    p.set_defaults(func=_cmd_info)

    return parser


def main(argv: list[str] | None = None) -> int:
    _setup_logging()
    banner()
    parser = build_parser()
    args = parser.parse_args(argv)

    func: Callable[[argparse.Namespace], None] = args.func
    try:
        func(args)
    except Bs9Error as exc:
        log.critical("Error: %s", exc)
        return 1
    except (OSError, ValueError) as exc:
        log.critical("Error: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
