import os
import shutil
import zipfile
from tqdm import tqdm
from rich import print

def split_string(s:str) -> list[str]:
    return [s[i:i+2] for i in range(0, len(s), 2)]

def get_content_from_file(file_path:str) -> str:
    if os.path.isfile(file_path):
        print("[bold green]File found.[/bold green]")
        with open(file_path, 'r', encoding='utf-8') as file:
            print("[bold green]Reading file...[/bold green]")
            content = file.read()
            return content
    else:
        print("[bold red]File not found[/bold red]")
        return "File not found"

def zipdir(path:str, ziph:zipfile.ZipFile) -> None:
    base_path = os.path.join(path, '..')
    dirs_created = set()
    all_dirs = set()
    
    all_files = []
    for root, _, files in os.walk(path):
        rel_dir = os.path.relpath(root, base_path).replace(os.sep, '/')
        all_dirs.add(rel_dir)
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, base_path).replace(os.sep, '/')
            all_files.append((full_path, rel_path))
    
    with tqdm(total=len(all_files), desc="Compressing files") as pbar:
        for full_path, rel_path in all_files:
            ziph.write(full_path, rel_path)
            
            parent = os.path.dirname(rel_path)
            while parent:
                dirs_created.add(parent)
                parent = os.path.dirname(parent)
            
            pbar.update(1)
    
    empty_dirs = [d for d in all_dirs if d and d not in dirs_created]
    if empty_dirs:
        with tqdm(total=len(empty_dirs), desc="Creating empty directories") as pbar:
            for rel_dir in empty_dirs:
                ziph.writestr(rel_dir + '/', '')
                pbar.update(1)

def delete_directory(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    else:
        print(f"[red]Error:[/red] [bold red]Can not find directory:[/bold red]{dir_path}")


def unzip_file(zip_path:str, extract_to:str) -> None:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_list = zip_ref.infolist()
        with tqdm(total=len(file_list), desc="Extracting") as pbar:
            for file in file_list:
                zip_ref.extract(file, extract_to)
                pbar.update(1)

def cut_filename(file_path:str) -> str:
    result = ""
    for i in range(len(file_path.split("/"))-1):
        result += file_path.split("/")[i] + "/"
    return result

def file_convert(original_path:str, target_path:str, code_number:int ,chunk_size:int=8192):
    try:
        file_size = os.path.getsize(original_path)
        
        with open(original_path, "rb") as src, open(target_path, "wb") as dst:
            with tqdm(total=file_size, unit='B', unit_scale=True, desc="Converting") as pbar:
                while True:
                    chunk = src.read(chunk_size)
                    if not chunk:
                        break
                    processed = bytes(b ^ code_number for b in chunk)
                    dst.write(processed)
                    pbar.update(len(chunk))
    except IOError as e:
        print(f'[red]Error:[/red] [bold red]{e}[/bold red]')
        raise

def copy_file(source_path:str, target_path:str):
    shutil.copy2(source_path, target_path)