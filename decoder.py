#code_super
#python -m nuitka --onefile --show-memory --show-progress --enable-plugin=pyside6 --remove-output --windows-icon-from-ico=./decoder.ico decoder.py
"""Decoder-only interactive menu (GUI file pickers)."""

import os
import subprocess
import sys

from rich import print
from PySide6.QtWidgets import QApplication, QFileDialog

from bs9 import default_codec, decode_file, unpack
from bs9.errors import Bs9Error
from bs9.ui import banner, error

BS9_FILTER = "bishop9910 files (*.bs9);;All files (*)"
BS9PCK_FILTER = "bishop9910 package files (*.bs9pck);;All files (*)"


def _pick_open(title: str, filters: str) -> str:
    path, _ = QFileDialog.getOpenFileName(None, title, "", filters)
    return path.replace(os.sep, "/") if path else ""


def main() -> None:
    banner()
    while True:
        print(
            "[blue]Enter the code[/blue] [bold red]1 for decode[/bold red],"
            "[bold blue]2 for unpack bs9pack[/bold blue],"
            "[bold green]3 for show data[/bold green],"
            "[bold purple]4 for exit[/bold purple]: "
        )
        try:
            code = input()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)

        if code == "1":
            path = _pick_open("Select the file", BS9_FILTER)
            if not path:
                continue
            try:
                new_name = decode_file(path)
            except Bs9Error as exc:
                error(str(exc))
                continue
            if os.path.splitext(new_name)[1].lstrip(".") == "html":
                subprocess.run(["start", new_name], shell=True)
                sys.exit(0)

        elif code == "2":
            path = _pick_open("Select the file", BS9PCK_FILTER)
            if not path:
                error("No file selected.")
                continue
            try:
                unpack(path)
            except Bs9Error as exc:
                error(str(exc))

        elif code == "3":
            default_codec.show_data()

        elif code == "4":
            sys.exit(0)

        else:
            error("Invalid input.")


app: QApplication = QApplication([])

if __name__ == "__main__":
    main()
