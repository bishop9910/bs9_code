#code_super_console
#python -m nuitka --onefile --show-memory --show-progress --enable-plugin=pyside6 --remove-output --windows-icon-from-ico=./console.ico console.py
from bs9Unpack import bs9Unpack
from decode_file import decode_file
from header import compute_header
from encode_file import encode_file
import logging
import sys
import os
from global_vals import global_vals
from bs9DEFAULTpack import bs9DEFAULTpack
from bs9HTMLpack import bs9HTMLpack

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'bs9_code_{global_vals.version}_csl.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def main() -> None:
    if len(sys.argv) < 2:
        logging.critical('Error: not enter any command.')
        sys.exit(1)

    command = sys.argv[1]

    if command == "--version":
        print(f"{global_vals.version}")
    elif command == "encode":
        filePath:str = ""
        if len(sys.argv) < 3:
            logging.critical('Error: no path entered.')
            sys.exit(1)
        else:
            filePath = sys.argv[2].replace(os.sep, '/')
        if filePath == '' or filePath == None:
            logging.critical('Error: target file not allowed.')
            sys.exit(1)

        typeAllowed: bool = False
        for t in global_vals.Textsuffix:
            if t == filePath.split('.')[-1]:
                typeAllowed = True

        if not typeAllowed:
            logging.critical('Error: target file not allowed.')
            sys.exit(1)

        logging.info(f"ENCODE COMMAND File: {filePath}, encoding...")
        newFilePath = encode_file(filePath)
        header = compute_header(newFilePath)
        fileType = header[0]
        readedVersion = header[1]
        convert_ID = header[2]
        convert_code = header[3]
        logging.info(f"{fileType=}")
        logging.info(f"{readedVersion=}")
        logging.info(f"{convert_ID=}")
        logging.info(f"{convert_code=}")
        logging.info("Encode Completed")
    elif command == "decode":
        filePath:str = ""
        if len(sys.argv) < 3:
            logging.critical('Error: no path entered.')
            sys.exit(1)
        else:
            filePath = sys.argv[2].replace(os.sep, '/')
        if filePath == '' or filePath == None:
            logging.critical('Error: target file not allowed.')
            sys.exit(1)
        if filePath.split('.')[-1] != 'bs9':
            logging.critical('Error: target file not allowed.')
            sys.exit(1)
        logging.info(f"DECODE COMMAND File: {filePath}, decoding...")
        header = compute_header(filePath)
        fileType = header[0]
        readedVersion = header[1]
        convert_ID = header[2]
        convert_code = header[3]
        logging.info(f"{fileType=}")
        logging.info(f"{readedVersion=}")
        logging.info(f"{convert_ID=}")
        logging.info(f"{convert_code=}")
        decode_file(filePath)
        os.remove(filePath)
        logging.info("Decode Completed")
    elif command == "pack":
        filePath:str = ""
        if len(sys.argv) < 3:
            logging.critical('Error: no path entered.')
            sys.exit(1)
        else:
            filePath = sys.argv[2].replace(os.sep, '/')
        if filePath == '' or filePath == None:
            logging.critical('Error: target path not allowed.')
            sys.exit(1)
        if not os.path.isdir(filePath):
            logging.critical('Error: target path not allowed.')
            sys.exit(1)
        logging.info(f"PACK COMMAND File: {filePath}, packing...")
        if os.path.isfile(filePath + "/index.html") or os.path.isfile(filePath + "/index.htm"):
            logging.info("It's a website folder")
            newFilePath = bs9HTMLpack(filePath)
        else:
            logging.info("It's a normal folder")
            newFilePath = bs9DEFAULTpack(filePath)
        header = compute_header(newFilePath)
        fileType = header[0]
        readedVersion = header[1]
        convert_ID = header[2]
        convert_code = header[3]
        logging.info(f"{fileType=}")
        logging.info(f"{readedVersion=}")
        logging.info(f"{convert_ID=}")
        logging.info(f"{convert_code=}")
        logging.info("Pack Completed")
    elif command == "unpack":
        filePath:str = ""
        if len(sys.argv) < 3:
            logging.critical('Error: no path entered.')
            sys.exit(1)
        else:
            filePath = sys.argv[2].replace(os.sep, '/')
        if filePath == '' or filePath == None:
            logging.critical('Error: target file not allowed.')
            sys.exit(1)
        if filePath.split('.')[-1] != 'bs9pck':
            logging.critical('Error: target file not allowed.')
            sys.exit(1)
        logging.info(f"UNPACK COMMAND File: {filePath}, unpacking...")
        header = compute_header(filePath)
        fileType = header[0]
        readedVersion = header[1]
        convert_ID = header[2]
        convert_code = header[3]
        logging.info(f"{fileType=}")
        logging.info(f"{readedVersion=}")
        logging.info(f"{convert_ID=}")
        logging.info(f"{convert_code=}")
        bs9Unpack(filePath)
        logging.info("Unpack Completed")
    else:
        logging.critical('Error: unkown command.')
        sys.exit(1)


if __name__ == "__main__":
    main()