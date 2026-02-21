#code_super 
#python -m nuitka --onefile --show-memory --show-progress --enable-plugin=pyside6 --remove-output --windows-icon-from-ico=./decoder.ico decoder.py
import subprocess
import sys
import os
from rich import print
from PySide6.QtWidgets import QApplication,QFileDialog
from bs9Unpack import bs9Unpack
from decode_file import decode_file
from global_vals import global_vals

app:QApplication = QApplication([])

#main thread
if __name__ == "__main__":
    while True:
        print(f"[bold blue]Bs9 Decoder[/bold blue] [white on red][[/white on red][white on blue]VERSION[/white on blue] {global_vals.version} [green]{global_vals.date}[/green][white on red]][/white on red] [green]by[/green] [white on purple]{global_vals.author}[/white on purple]")
        print("[blue]Enter the code[/blue] [bold red]1 for decode[/bold red],[bold blue]2 for unpack bs9pack[/bold blue],[bold green]3 for show data[/bold green],[bold purple]4 for exit[/bold purple]: ")
        code:str = input()
        if code == "1":
            e_file_path, _ = QFileDialog.getOpenFileName(None,"Select the file",'',"bishop9910 files (*.bs9);;All files (*)")
            rel_e_path = e_file_path.replace(os.sep, '/')
            new_filename:str = decode_file(rel_e_path)
            if new_filename == "Error":
                continue
            if(new_filename.split(".")[-1] == "html"):
                html_file_path:str = new_filename
                subprocess.run(["start", html_file_path], shell=True)
                sys.exit(0)
        elif code == "2":
            file_path, _ = QFileDialog.getOpenFileName(None,"Select the file",'',"bishop9910 package files (*.bs9pck);;All files (*)")
            if file_path == "":
                print("[red]Error:[/red] [bold red]No file selected.[/bold red]")
                continue
            rel_file_path = file_path.replace(os.sep, '/')
            bs9Unpack(rel_file_path)
        elif code == "3":
            global_vals.data_obj.show_data()
        elif code == "4":
            sys.exit(0)
        else:
            print("[red]Error:[/red] [bold red]Invalid input.[/bold red]")