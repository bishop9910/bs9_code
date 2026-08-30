#bs9FileInfoReader
#python -m nuitka --onefile --show-memory --show-progress --enable-plugin=pyside6 --remove-output --windows-icon-from-ico=./bs9FileInfoReader.ico bs9FileInfoReader.py
"""Show the header info of a .bs9 / .bs9pck file (GUI picker or argv)."""

import os
import sys

from PySide6.QtWidgets import QApplication, QFileDialog

from bs9 import compute_header
from bs9.errors import Bs9Error


def _pick_file() -> str:
    path, _ = QFileDialog.getOpenFileName(
        None,
        "Select the file",
        "",
        "bishop9910 files (*.bs9);;bishop9910 package files (*.bs9pck);;All files (*)",
    )
    return path


def main() -> None:
    app = QApplication([])

    file_path = ""
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        file_path = sys.argv[1]
    else:
        file_path = _pick_file()

    if not file_path:
        print("Error: Not select a file.")
        sys.exit(1)

    try:
        print(compute_header(file_path).display())
    except Bs9Error as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    input()


if __name__ == "__main__":
    main()
