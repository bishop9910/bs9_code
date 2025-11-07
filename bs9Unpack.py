import os
import sys
import subprocess
from tqdm import tqdm
from decode_file import decode_file
from methods import cut_filename, file_convert, unzip_file, copy_file
from header import compute_header, remove_header
from rich import print
from global_vals import version

def bs9Unpack(file_path:str) -> None:
    filename:str = ""
    header = compute_header(file_path)
    fileType = header[0]
    if fileType != 'bs9pck':
        print("[red]Error:[/red] [bold red]Coded version too low, try a lower decoder to decode it.[/bold red]")
        return None
    readedVersion = header[1]
    if readedVersion != version:
        print("[red]Error:[/red] [bold red]Coded file's version not supported.[/bold red]")
        return None
    convert_code = int(header[3])
    print("[blue]Unpacking...[/blue]")
    for i in file_path.split("/")[-1].split("."):
        if i == "bs9pck":
            break
        elif i == file_path.split("/")[-1].split(".")[0]:
            filename += i
        else:
            filename += "." + i
    folder_path:str = cut_filename(file_path)
    ziped_file:str = folder_path + filename + ".zip"
    no_header_file_path:str = file_path + '.noheader'
    copy_file(file_path, no_header_file_path)
    remove_header(no_header_file_path)
    file_convert(no_header_file_path, ziped_file, convert_code)
    unzip_file(ziped_file, folder_path)
    paths:object = os.walk(folder_path + filename)
    launcher_file:str = ""
    index_file:str = ""
    all_files:list[str] = []
    for dirpath, _, filenames in paths:
        dirpath = dirpath.replace(os.sep,'/')
        for filename_ in filenames:
            filePath:str = dirpath + '/' + filename_
            all_files.append(filePath)
    with tqdm(total=len(all_files), desc="Decoding files") as pbar:
        for filePath in all_files:
            if os.path.isfile(filePath):
                print(filePath)
                if filePath.split(".")[-1] == "bs9":
                    decode_file(filePath)
                    os.remove(filePath)
                if filePath.split("/")[-1] == "launcher_9910.exe":
                    launcher_file = filePath
            pbar.update(1)
    if os.path.isfile(folder_path + filename + '/index.html'):
        index_file = folder_path + filename + '/index.html'
    elif os.path.isfile(folder_path + filename + '/index.htm'):
        index_file = folder_path + filename + '/index.htm'
    os.remove(ziped_file)
    os.remove(no_header_file_path)
    os.remove(file_path)
    if launcher_file != "" and index_file != "":
        print("[bold green]Unpack Completed[/bold green]")
        try:
            subprocess.run(["start", launcher_file], shell=True)
            sys.exit(0)
        except Exception as e:
            print(f"[red]Error:[/red] [bold red]{e}[/bold red]")
    else:
        print("[bold green]Unpack Completed[/bold green]")