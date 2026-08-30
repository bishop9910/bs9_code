"""Shared constants for the bs9 file format.

Everything that used to be scattered across ``global_vals.py`` lives here so
that the four executables (and any future tool) agree on the version, header
layout and supported suffixes.
"""

from __future__ import annotations

# Build / identity -----------------------------------------------------------
VERSION: str = "1.3.100"
DATE: str = "2026/08/30"
AUTHOR: str = "bishop9910"

# Which character table this build uses.  The name is embedded in every
# encoded file so a decoder can refuse incompatible tables.
CODER_VERSION: str = "data_0x9910"

# File suffixes that are treated as encodable text (used by pack + CLI).
TEXT_SUFFIXES: tuple[str, ...] = (
    "txt", "js", "html", "css", "md", "ts", "py", "c", "cpp",
)

# Encoded-file suffixes ------------------------------------------------------
BS9_SUFFIX: str = "bs9"
BS9PCK_SUFFIX: str = "bs9pck"

# Every .bs9 / .bs9pck file starts with a fixed-size plain-text header.
HEADER_SIZE: int = 22

# The per-file XOR key is derived from a random hex value stored in the
# header:  xor_key = int(hex_value, 16) // XOR_KEY_DIVISOR
XOR_KEY_DIVISOR: int = 5891

# Website-launcher payload used by the HTML packer (paths are relative to the
# process working directory, matching the original behaviour).
LAUNCHER_PACK: str = "data.bs9pck"
LAUNCHER_DATA_DIR: str = "data"
LAUNCHER_EXE: str = "launcher.exe"
WEBVIEW2_DLL: str = "WebView2Loader.dll"
