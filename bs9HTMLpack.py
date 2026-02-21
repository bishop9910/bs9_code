import os
import shutil
import zipfile
from global_vals import global_vals
from encode_file import encode_file
from methods import zipdir, file_convert, delete_directory
from rich import print
from header import get_bs9pck_header, insert_header_mmap
from bs9Unpack import bs9Unpack
from bs9DEFAULTpack import bs9DEFAULTpack

def bs9HTMLpack(folder_path:str) -> str:
    print(folder_path)
    if os.path.exists("data.bs9pck"):
        print("[bold purple]Main data found[/bold purple]")
    else:
        print("[red]Err:[/red] [bold red]Main data not found[/bold red]")
        return ''
    try:
        paths:object = os.walk(folder_path)
        for dirpath, _, filenames in paths:
            dirpath = dirpath.replace(os.sep,'/')
            for filename in filenames:
                file_path = dirpath + '/' + filename
                if os.path.isfile(file_path):
                    print(file_path)
                    for i in global_vals.Textsuffix:
                        if filename.split('.')[-1] == i:
                            encode_file(file_path)
                            os.remove(file_path)
        bs9Unpack('./data.bs9pck')
        src_file:str = "./data/launcher.exe"
        dll_filr:str = "./data/WebView2Loader.dll"
        dst_folder:str = folder_path
        dst_assets_dir = folder_path + '/' + "assets"
        if os.path.exists(dst_folder + '/' + "launcher.exe") or os.path.exists(dst_folder + '/' + "WebView2Loader.dll") or os.path.exists(dst_assets_dir):
            os.remove(dst_folder + '/' + "launcher.exe")
            os.remove(dst_folder + '/' + "WebView2Loader.dll")
            os.removedirs(dst_assets_dir)
        os.makedirs(dst_assets_dir, exist_ok=True)
        for item in os.listdir(folder_path):
            src_item = os.path.join(folder_path, item)
            if item in ["assets", "launcher.exe", "WebView2Loader.dll"]:
                continue
            dst_item = os.path.join(dst_assets_dir, item)
            shutil.move(src_item, dst_item)
        shutil.copy(src_file, dst_folder)
        shutil.copy(dll_filr, dst_folder)
        zipf:zipfile.ZipFile = zipfile.ZipFile(folder_path + ".zip", 'w', zipfile.ZIP_DEFLATED)
        zipdir(folder_path, zipf)
        zipf.close()
        ziped_file:str = folder_path + ".zip"
        final_filename:str = folder_path + ".bs9pck"
        bs9pck_header = None
        convert_code = 0
        print("[bold blue]New file name:[/bold blue] ", final_filename)
        while True:
            bs9pck_header = get_bs9pck_header()  # 生成 header
            try:
                header_str = bs9pck_header.decode('utf-8')
                xor_hex = header_str.split('_')[2]
                convert_code = int(xor_hex, 16) // 5891
                if convert_code != 0:
                    break
            except Exception:
                continue
        file_convert(ziped_file, final_filename, convert_code)
        insert_header_mmap(final_filename, bs9pck_header)
        delete_directory(folder_path)
        os.remove(ziped_file)
        print("[bold green]Pack Completed[/bold green]")
        return final_filename
    except Exception as e:
        print(f"[red]Error:[/red] [bold red]{e}[/bold red]")
        return ''
    finally:
        bs9DEFAULTpack('./data')