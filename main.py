#code_super
#python -m nuitka --onefile --show-memory --show-progress --enable-plugin=pyside6 --remove-output --windows-icon-from-ico=./main.ico main.py
"""Interactive encoder/decoder menu (GUI file pickers).

Thin entry point; all format logic lives in the :mod:`bs9` package.
"""

import os
import subprocess
import sys

from rich import print
from PySide6.QtWidgets import QApplication, QFileDialog

from bs9 import default_codec, decode_file, encode_file, pack, unpack
from bs9.errors import Bs9Error
from bs9.ui import banner, error, menu_help

TEXT_FILTER = (
    "Text files (*.txt);;HTML files (*.html);;Javascript files (*.js);;"
    "Ini files (*.ini);;Toml files (*.toml);;JSON files (*.json);;All files (*)"
)
BS9_FILTER = "bishop9910 files (*.bs9);;All files (*)"
BS9PCK_FILTER = "bishop9910 package files (*.bs9pck);;All files (*)"


def _pick_open(title: str, filters: str) -> str:
    path, _ = QFileDialog.getOpenFileName(None, title, "", filters)
    return path.replace(os.sep, "/") if path else ""


def _pick_folder(title: str) -> str:
    path = QFileDialog.getExistingDirectory(None, title)
    return path.replace(os.sep, "/") if path else ""


def main() -> None:
    banner()
    while True:
        print(
            "[blue]Enter the code[/blue] [white on red]([/white on red]"
            "[bold red]0 for help,[/bold red]"
            "[bold green]1 for encode text file,[/bold green]"
            "[bold blue]2 for decode bs9 file,[/bold blue]"
            "[bold purple]3 for show data,[/bold purple]"
            "[bold red]4 for make bs9pack,[/bold red]"
            "[bold green]5 for unpack bs9pack,[/bold green]"
            "[bold blue]6 for encode texts,[/bold blue]"
            "[bold red]7 for decode bs9 texts,[/bold red]"
            "[bold green]8 for exit[/bold green][white on red])[/white on red]: "
        )
        try:
            code = input()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)

        if code == "0":
            menu_help()

        elif code == "1":
            path = _pick_open("Select the file", TEXT_FILTER)
            if not path:
                error("No file selected.")
                continue
            try:
                encode_file(path)
            except Bs9Error as exc:
                error(str(exc))

        elif code == "2":
            path = _pick_open("Select the file", BS9_FILTER)
            if not path:
                error("No file selected.")
                continue
            try:
                new_name = decode_file(path)
            except Bs9Error as exc:
                error(str(exc))
                continue
            if os.path.splitext(new_name)[1].lstrip(".") in ("html", "htm"):
                subprocess.run(["start", new_name], shell=True)
                sys.exit(0)

        elif code == "3":
            default_codec.show_data()

        elif code == "4":
            folder = _pick_folder("Select the folder")
            if not folder:
                error("No folder selected.")
                continue
            print(f"[blue]You choosed:[/blue] {folder}[green], packing...[/green]")
            try:
                pack(folder)
            except Bs9Error as exc:
                error(str(exc))

        elif code == "5":
            path = _pick_open("Select the file", BS9PCK_FILTER)
            if not path:
                error("No file selected.")
                continue
            try:
                unpack(path)
            except Bs9Error as exc:
                error(str(exc))

        elif code == "6":
            print("[blue]Enter the text you want to encode:[/blue]")
            print(default_codec.encode(input()))

        elif code == "7":
            print("[blue]Enter the text which is encoded by this version's encoder:[/blue]")
            print(default_codec.decode(input()))

        elif code == "8":
            sys.exit(0)

        else:
            error("Invalid input.")


app: QApplication = QApplication([])

if __name__ == "__main__":
    main()
