"""Folder packing/unpacking (.bs9pck).

A ``.bs9pck`` is a ZIP archive of a folder (with the folder's own name as the
archive root), XORed with the per-file key and given a fixed header — exactly
like a ``.bs9`` file but for a whole directory tree.

The website variant additionally injects ``launcher.exe`` +
``WebView2Loader.dll`` (unpacked from :data:`~bs9.constants.LAUNCHER_PACK`)
into the archive root and moves the site files under ``assets/``.
"""

from __future__ import annotations

import logging
import os
import shutil
import zipfile

from tqdm import tqdm

from .constants import (
    BS9PCK_SUFFIX,
    LAUNCHER_DATA_DIR,
    LAUNCHER_EXE,
    LAUNCHER_PACK,
    TEXT_SUFFIXES,
    VERSION,
    WEBVIEW2_DLL,
)
from .errors import DecodeError, PackError
from .file_codec import decode_file, encode_file
from .files import (
    copy_file,
    delete_directory,
    remove_file,
    unzip_file,
    xor_file,
    zip_directory,
)
from .header import compute_header, insert_header, make_header, parse_header, remove_header
from .tables import Codec, default_codec

log = logging.getLogger("bs9.pack")


def _encode_text_files(folder_path: str, codec: Codec) -> None:
    """Walk ``folder_path`` and replace every text file with its .bs9 form."""
    for dirpath, _, filenames in os.walk(folder_path):
        dirpath = dirpath.replace(os.sep, "/")
        for name in filenames:
            if name.rsplit(".", 1)[-1] in TEXT_SUFFIXES:
                file_path = dirpath + "/" + name
                encode_file(file_path, codec=codec)
                remove_file(file_path)


def _finalize_archive(folder_path: str, remove_source: bool) -> str:
    """Zip ``folder_path``, then XOR + header it into ``<folder>.bs9pck``."""
    zip_path = folder_path + ".zip"
    final_path = folder_path + "." + BS9PCK_SUFFIX

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zip_directory(folder_path, zf)

    header = make_header(BS9PCK_SUFFIX)
    xor_key = parse_header(header).xor_key

    xor_file(zip_path, final_path, xor_key)
    insert_header(final_path, header)

    if remove_source:
        delete_directory(folder_path)
    remove_file(zip_path)
    return final_path


def _pack_folder(folder_path: str, *, codec: Codec, remove_source: bool) -> str:
    """Pack a normal (non-website) folder into a ``.bs9pck``."""
    log.info("Packing normal folder %s", folder_path)
    _encode_text_files(folder_path, codec)
    return _finalize_archive(folder_path, remove_source)


def _pack_website(folder_path: str, *, codec: Codec, remove_source: bool) -> str:
    """Pack a website folder, injecting the launcher payload."""
    if not os.path.exists(LAUNCHER_PACK):
        raise PackError(f"main data not found: {LAUNCHER_PACK!r}")

    assets_dir = folder_path + "/assets"
    if os.path.exists(assets_dir):
        # Already prepared (launcher previously injected) — pack as normal.
        return _pack_folder(folder_path, codec=codec, remove_source=remove_source)

    log.info("Packing website folder %s", folder_path)
    _encode_text_files(folder_path, codec)

    data_unpacked = False
    try:
        # Unpack the launcher payload into ./data (kept for re-packing below).
        unpack(LAUNCHER_PACK, remove_source=False)
        data_unpacked = True

        src_exe = f"{LAUNCHER_DATA_DIR}/{LAUNCHER_EXE}"
        src_dll = f"{LAUNCHER_DATA_DIR}/{WEBVIEW2_DLL}"

        for name in (LAUNCHER_EXE, WEBVIEW2_DLL):
            stale = folder_path + "/" + name
            if os.path.exists(stale):
                os.remove(stale)

        os.makedirs(assets_dir, exist_ok=True)
        for item in os.listdir(folder_path):
            if item in ("assets", LAUNCHER_EXE, WEBVIEW2_DLL):
                continue
            shutil.move(os.path.join(folder_path, item), os.path.join(assets_dir, item))

        shutil.copy(src_exe, folder_path)
        shutil.copy(src_dll, folder_path)

        return _finalize_archive(folder_path, remove_source)
    finally:
        if data_unpacked:
            # Restore the launcher payload archive and remove ./data.
            _pack_folder(LAUNCHER_DATA_DIR, codec=codec, remove_source=True)


def pack(folder_path: str, *, codec: Codec = default_codec,
         website: bool | None = None, remove_source: bool = True) -> str:
    """Pack a folder into a ``.bs9pck``, auto-detecting website folders.

    Parameters
    ----------
    website:
        ``True`` forces the website (launcher) path, ``False`` forces the
        normal path, ``None`` auto-detects from the presence of ``index.html``
        / ``index.htm``.
    remove_source:
        Delete the source folder after packing (original default behaviour).
    """
    folder_path = os.path.abspath(folder_path)
    if not os.path.isdir(folder_path):
        raise PackError(f"not a directory: {folder_path}")

    if website is None:
        website = (
            os.path.isfile(folder_path + "/index.html")
            or os.path.isfile(folder_path + "/index.htm")
        )

    if website:
        return _pack_website(folder_path, codec=codec, remove_source=remove_source)
    return _pack_folder(folder_path, codec=codec, remove_source=remove_source)


def _folder_base_name(file_path: str) -> str:
    """Return the folder name a ``.bs9pck`` restores to (strip ``.bs9pck``)."""
    return os.path.splitext(os.path.basename(file_path))[0]


def unpack(file_path: str, *, codec: Codec = default_codec,
           remove_source: bool = True) -> str:
    """Unpack a ``.bs9pck`` back into a folder next to the archive.

    Returns the absolute path of the extracted folder.  With
    ``remove_source=True`` (the default) the source ``.bs9pck`` is deleted.
    """
    file_path = os.path.abspath(file_path)
    header = compute_header(file_path)
    if header.file_type != BS9PCK_SUFFIX:
        raise DecodeError("coded version too low, try a lower decoder to decode it.")
    if header.version != VERSION:
        raise DecodeError("coded file's version not supported.")

    folder_name = _folder_base_name(file_path)
    parent = os.path.dirname(file_path)
    zip_path = os.path.join(parent, folder_name + ".zip")
    no_header_path = file_path + ".noheader"

    log.info("Unpacking %s", file_path)
    copy_file(file_path, no_header_path)
    remove_header(no_header_path)
    xor_file(no_header_path, zip_path, header.xor_key)
    unzip_file(zip_path, parent)

    extracted_root = os.path.join(parent, folder_name)
    launcher_file = ""
    index_file = ""

    all_files: list[str] = []
    for dirpath, _, filenames in os.walk(extracted_root):
        dirpath = dirpath.replace(os.sep, "/")
        for name in filenames:
            all_files.append(dirpath + "/" + name)

    with tqdm(total=len(all_files), desc="Decoding files") as pbar:
        for path in all_files:
            if not os.path.isfile(path):
                pbar.update(1)
                continue
            if path.rsplit(".", 1)[-1] == "bs9":
                decode_file(path, codec=codec)
                remove_file(path)
            if os.path.basename(path) == LAUNCHER_EXE:
                launcher_file = path
            pbar.update(1)

    if os.path.isfile(extracted_root + "/assets/index.html"):
        index_file = extracted_root + "/assets/index.html"
    elif os.path.isfile(extracted_root + "/assets/index.htm"):
        index_file = extracted_root + "/assets/index.htm"

    remove_file(zip_path)
    remove_file(no_header_path)
    if remove_source:
        remove_file(file_path)

    log.info("Unpacked to %s", extracted_root)
    return extracted_root
