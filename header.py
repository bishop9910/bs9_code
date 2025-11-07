from global_vals import bs9_header_info, bs9pck_header_info
import random
import os
import mmap

def header_maker(info: str) -> bytes:
    if not info or '_' not in info:
        raise ValueError("info must be a non-empty string containing '_'")

    prefix = info.split('_')[0]
    if prefix not in ('bs9', 'bs9pck'):
        raise ValueError("info must start with 'bs9' or 'bs9pck'")

    rand_hex = hex(random.randint(100_000, 999_999))

    if prefix == 'bs9':
        header_str = f"{info}{rand_hex}_"
        padding = b'\x00' * 2
    else:
        header_str = f"{info}{rand_hex}"
        padding = b''

    return header_str.encode('utf-8') + padding

def get_bs9_header():
    bs9_header = header_maker(bs9_header_info)
    return bs9_header

def get_bs9pck_header():
    bs9pck_header = header_maker(bs9pck_header_info)
    return bs9pck_header

def compute_header(filePath:str) -> list[str]:
    header = read_header(filePath)
    info = header.decode('utf-8').split('_')
    fileType = info[0]
    readedVersion = info[1]
    convert_ID = f'{info[2]}(hex)'
    convert_code = str(int(info[2], 16)//5891)
    return [fileType, readedVersion, convert_ID, convert_code]

def insert_header_mmap(filename:str, header_data:bytes) -> None:
    assert len(header_data) == 22, "Header must be 22 bytes"
    
    orig_size = os.path.getsize(filename)
    
    with open(filename, 'r+b') as f:
        f.seek(0, os.SEEK_END)
        f.write(b'\x00' * 22)
        f.flush()
        
        mm = mmap.mmap(f.fileno(), orig_size + 22, access=mmap.ACCESS_WRITE)
        mm.move(22, 0, orig_size)
        mm.seek(0)
        mm.write(header_data)
        mm.close()

def remove_header(filename:str, header_size:int=22) -> None:
    temp_file = filename + '.tmp'
    
    with open(filename, 'rb') as orig, open(temp_file, 'wb') as tmp:
        orig.seek(header_size)
        
        chunk_size = 1024 * 1024
        while True:
            chunk = orig.read(chunk_size)
            if not chunk:
                break
            tmp.write(chunk)
    
    os.replace(temp_file, filename)

def read_header(filename:str) -> bytes:
    with open(filename, 'rb') as f:
        content = f.read(22)
    return content

if __name__ == '__main__':
    print(len(get_bs9_header()), get_bs9_header())
    print(len(get_bs9pck_header()), get_bs9pck_header())