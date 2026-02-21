import os
from global_vals import global_vals
from methods import get_content_from_file, file_convert
from header import get_bs9_header, insert_header_mmap
from rich import print
from encode import encode

def encode_file(o_file_path:str) -> str:
    try:
        if o_file_path == "":
            print("[red]Error:[/red] [bold red]No file selected.[/bold red]")
            return ""
        string:str = get_content_from_file(o_file_path)
        output:str = encode(string)
        o_file_type:str = "." + o_file_path.split(".")[-1]
        output += "." + global_vals.coder_version + o_file_type
        filename:str = o_file_path+".temp"
        print("[bold purple]Temp file name:[/bold purple] ",filename)
        with open(filename, "w" , encoding='utf-8') as f:
            f.write(output)
        print("[bold green]Create temp file successfully[/bold green]")
        new_filename:str = ""
        for i in o_file_path.split("."):
            if i == o_file_path.split(".")[-1]:
                break
            elif i == o_file_path.split(".")[0]:
                new_filename += i
            else:
                new_filename += "." + i
        new_filename += ".bs9"
        bs9_header = None
        convert_code = 0
        print("[bold blue]New file name:[/bold blue] ", new_filename)
        while True:
            bs9_header = get_bs9_header()  # 生成 header
            try:
                header_str = bs9_header.decode('utf-8')
                xor_hex = header_str.split('_')[2]
                convert_code = int(xor_hex, 16) // 5891
                if convert_code != 0:
                    break
            except Exception:
                continue
        file_convert(filename, new_filename, convert_code)
        insert_header_mmap(new_filename, bs9_header)
        os.remove(filename)  
        print("[bold green]Encode Completed[/bold green]")
        return new_filename
    except:
        print("[red]Error:[/red] [bold red]Invalid file path or invalid file type or content[/bold red]")
        return ""
