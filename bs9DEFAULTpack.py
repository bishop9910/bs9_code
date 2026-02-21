import os
import zipfile
from global_vals import global_vals
from methods import zipdir, file_convert, delete_directory
from encode_file import encode_file
from rich import print
from header import get_bs9pck_header, insert_header_mmap

def bs9DEFAULTpack(folder_path:str) -> str:
    print(folder_path)
    try:
        paths:object = os.walk(folder_path)
        for dirpath, _, filenames in paths:
            dirpath = dirpath.replace(os.sep,'/')
            for filename in filenames:
                file_path:str = dirpath + '/' + filename
                if os.path.isfile(file_path):
                    print(file_path)
                    for i in global_vals.Textsuffix:
                        if filename.split('.')[-1] == i:
                            encode_file(file_path)
                            os.remove(file_path)
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