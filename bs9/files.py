"""Low-level file helpers: text reading, XOR transform, zip utilities."""

from __future__ import annotations

import os
import shutil
import zipfile

from tqdm import tqdm

_CHUNK_SIZE = 64 * 1024


def read_text_file(path: str) -> str:
    """Read a UTF-8 text file and return its contents.

    Raises :class:`OSError` (and therefore propagates a clear error) instead of
    returning the string ``"File not found"`` like the original helper.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def copy_file(source: str, target: str) -> None:
    """Copy a file preserving metadata (thin wrapper over ``shutil.copy2``)."""
    shutil.copy2(source, target)


def _xor_table(key: int) -> bytes:
    """Build a 256-byte translation table for a single-byte XOR key."""
    return bytes(i ^ key for i in range(256))


def xor_file(source: str, target: str, key: int, chunk_size: int = _CHUNK_SIZE) -> None:
    """XOR every byte of ``source`` with ``key`` and write the result to ``target``.

    Uses ``bytes.translate`` with a precomputed table instead of a per-byte
    Python generator, which is dramatically faster for large files.
    """
    table = _xor_table(key)
    total = os.path.getsize(source)
    with open(source, "rb") as src, open(target, "wb") as dst:
        with tqdm(total=total, unit="B", unit_scale=True, desc="Converting") as pbar:
            while True:
                chunk = src.read(chunk_size)
                if not chunk:
                    break
                dst.write(chunk.translate(table))
                pbar.update(len(chunk))


def zip_directory(path: str, zf: zipfile.ZipFile) -> None:
    """Write the contents of ``path`` into ``zf`` with ``path``'s own name as
    the archive root (so extracting next to the source restores the folder).
    """
    parent = os.path.dirname(os.path.abspath(path))
    files: list[tuple[str, str]] = []
    all_dirs: set[str] = set()

    for root, _, names in os.walk(path):
        rel_dir = os.path.relpath(root, parent).replace(os.sep, "/")
        all_dirs.add(rel_dir)
        for name in names:
            full = os.path.join(root, name)
            rel = os.path.relpath(full, parent).replace(os.sep, "/")
            files.append((full, rel))

    created_dirs: set[str] = set()
    with tqdm(total=len(files), desc="Compressing files") as pbar:
        for full, rel in files:
            zf.write(full, rel)
            d = os.path.dirname(rel)
            while d:
                created_dirs.add(d)
                d = os.path.dirname(d)
            pbar.update(1)

    empty_dirs = [d for d in all_dirs if d and d not in created_dirs]
    if empty_dirs:
        with tqdm(total=len(empty_dirs), desc="Creating empty directories") as pbar:
            for rel_dir in empty_dirs:
                zf.writestr(rel_dir + "/", "")
                pbar.update(1)


def unzip_file(zip_path: str, extract_to: str) -> None:
    """Extract ``zip_path`` into ``extract_to``, guarding against zip-slip."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        members = zf.infolist()
        with tqdm(total=len(members), desc="Extracting") as pbar:
            for member in members:
                target = os.path.normpath(os.path.join(extract_to, member.filename))
                base = os.path.normpath(extract_to)
                if os.path.commonpath([base, target]) != base:
                    raise ValueError(f"unsafe path in archive: {member.filename!r}")
                zf.extract(member, extract_to)
                pbar.update(1)


def delete_directory(path: str) -> None:
    """Recursively delete ``path`` if it exists."""
    if os.path.isdir(path):
        shutil.rmtree(path)


def remove_file(path: str) -> None:
    """Remove ``path`` if it exists (no error when already gone)."""
    if os.path.isfile(path):
        os.remove(path)
