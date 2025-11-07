#code_super
#python -m nuitka --onefile --show-memory --show-progress --enable-plugin=pyside6 --remove-output --windows-icon-from-ico=./main.ico main.py
import os
import subprocess
import sys
from rich import print
from PySide6.QtWidgets import QApplication,QFileDialog
from bs9Help import printHelp
from bs9DEFAULTpack import bs9DEFAULTpack
from bs9HTMLpack import bs9HTMLpack
from bs9Unpack import bs9Unpack
from decode_file import decode_file
from encode_file import encode_file
from decode import decode
from encode import encode
from global_vals import version, date, data_obj


app:QApplication = QApplication([])

#main thread
if __name__ == "__main__":
    while True:
        print(f"[bold blue]Bs9 Encoder/Decoder[/bold blue] [white on red][[/white on red][white on blue]VERSION[/white on blue] {version} [green]{date}[/green][white on red]][/white on red] [green]by[/green] [white on purple]Bishop9910[/white on purple]")
        print("[blue]Enter the code[/blue] [white on red]([/white on red][bold red]0 for help,[/bold red][bold green]1 for encode text file,[/bold green][bold blue]2 for decode bs9 file,[/bold blue][bold purple]3 for show data,[/bold purple][bold red]4 for make bs9pack,[/bold red][bold green]5 for unpack bs9pack,[/bold green][bold blue]6 for encode texts,[/bold blue][bold red]7 for decode bs9 texts,[/bold red][bold green]8 for exit[/bold green][white on red])[/white on red]: ")
        code:str = input()
        if code == "0":
            printHelp()
        elif code == "1":
            o_file_path,_ = QFileDialog.getOpenFileName(None,"Select the file",'',"Text files (*.txt);;HTML files (*.html);;Javascript files (*.js);;Ini files (*.ini);;Toml files (*.toml);;JSON files (*.json);;All files (*)")
            rel_o_path = o_file_path.replace(os.sep, '/')
            encode_file(rel_o_path)
        elif code == "2":
            e_file_path,_ = QFileDialog.getOpenFileName(None,"Select the file",'',"bishop9910 files (*.bs9);;All files (*)")
            rel_e_path = e_file_path.replace(os.sep, '/')
            new_filename:str = decode_file(rel_e_path)
            if new_filename == "Error":
                continue
            if(new_filename.split(".")[-1] == "html" or new_filename.split(".")[-1] == "htm"):
                html_file_path:str = new_filename
                subprocess.run(["start", html_file_path], shell=True)
                sys.exit(0)
        elif code == "3":
            data_obj.show_data()
        elif code == "4":
            folder_path = QFileDialog.getExistingDirectory(None,'Select the folder')
            if folder_path == "":
                print("[red]Error:[/red] [bold red]No folder selected.[/bold red]")
                continue
            rel_folder_path = folder_path.replace(os.sep, '/')
            print(f"[blue]You choosed:[/blue] {rel_folder_path}[green], packing...[/green]")
            if os.path.isfile(rel_folder_path + "/index.html") or os.path.isfile(rel_folder_path + "/index.htm"):
                print("[purple]It's a website folder[/purple]")
                bs9HTMLpack(rel_folder_path)
            else:
                print("[purple]It's a normal folder[/purple]")
                bs9DEFAULTpack(rel_folder_path)
        elif code == "5":
            file_path,_ = QFileDialog.getOpenFileName(None,"Select the file",'',"bishop9910 package files (*.bs9pck);;All files (*)")
            if file_path == "":
                print("[red]Error:[/red] [bold red]No file selected.[/bold red]")
                continue
            rel_file_path = file_path.replace(os.sep, '/')
            bs9Unpack(rel_file_path)
        elif code == "6":
            print("[blue]Enter the text you want to encode:[/blue]")
            text:str = input()
            output = encode(text)
            print(output)
        elif code == "7":
            print("[blue]Enter the text which is encoded by this version's encoder:[/blue]")
            text:str = input()
            output = decode(text)
            print(output)
        elif code == "8":
            sys.exit(0)
        else:
            print("[red]Error:[/red] [bold red]Invalid input.[/bold red]")