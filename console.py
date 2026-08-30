#code_super_console
#python -m nuitka --onefile --show-memory --show-progress --enable-plugin=pyside6 --remove-output --windows-icon-from-ico=./console.ico console.py
"""Bs9 command-line tool.

Thin entry point; all logic lives in :mod:`bs9.cli`.
"""

from bs9.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
