import os
from global_vals import global_vals
from methods import file_convert, get_content_from_file, copy_file
from header import compute_header, remove_header
from rich import print
from decode import decode

def decode_file(e_file_path:str) -> str:
    try:
        if e_file_path == "":
            print("[red]Error:[/red] [bold red]No file selected.[/bold red]")
            return "Error"
        header = compute_header(e_file_path)
        fileType = header[0]
        if fileType != 'bs9':
            print("[red]Error:[/red] [bold red]Coded version too low, try a lower decoder to decode it.[/bold red]")
            return "Error"
        readedVersion = header[1]
        if readedVersion != global_vals.version:
            print("[red]Error:[/red] [bold red]Coded file's version not supported.[/bold red]")
            return "Error"
        convert_code = int(header[3])
        print(e_file_path,"[blue]decoding...[/blue]")
        no_header_file_path:str = e_file_path + '.noheader'
        copy_file(e_file_path, no_header_file_path)
        remove_header(no_header_file_path)
        filename:str = e_file_path + ".temp"
        print("[bold purple]Temp file name:[/bold purple] ",filename)
        file_convert(no_header_file_path, filename, convert_code)
        print("[bold green]Create temp file successfully[/bold green]")
        encoded_content:str = get_content_from_file(filename)
        content:str = encoded_content.split(".")[0]
        data_version:str = encoded_content.split(".")[1]
        if(data_version != global_vals.coder_version):
            print("[red]Error:[/red] [bold red]The encoded content version is not as the same as the decoder's.[/bold red]")
            return "Error"
        e_file_type:str = "." + encoded_content.split(".")[2]
        output:str = decode(content)
        new_filename:str = ""
        for i in e_file_path.split("."):
            if i == "bs9":
                break
            elif i == e_file_path.split(".")[0]:
                new_filename += i
            else:
                new_filename += "." + i
        new_filename += e_file_type
        print("[bold blue]New file name:[/bold blue] ", new_filename)
        with open(new_filename, "w", encoding='utf-8') as f:
            f.write(output)
        os.remove(no_header_file_path)
        os.remove(filename)
        print("[bold green]Decode Completed[/bold green]")
        return new_filename
    except:
        print("[red]Error:[/red] [bold red]Invalid file path or invalid file type or content[/bold red]")
        return "Error"