#code_super_console
#python -m nuitka --onefile --show-memory --show-progress --enable-plugin=pyside6 --remove-output --windows-icon-from-ico=./console.ico console.py
from bs9Unpack import bs9Unpack
from decode_file import decode_file
from header import compute_header
from encode_file import encode_file
import logging
import sys
import os
from global_vals import version
from bs9DEFAULTpack import bs9DEFAULTpack
from bs9HTMLpack import bs9HTMLpack

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'code_{version}_csl.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def main() -> None:
    filePath:str = ""
    if len(sys.argv) != 1:
        preFilePath = sys.argv[1]
        filePath  = preFilePath.replace(os.sep, '/')
    else:
        logging.critical('Error: Not select a target file.')

    if filePath == '' or filePath == None:
        logging.critical('Error: Target file not allowed.')
        sys.exit(1)

    if os.path.isdir(filePath):
        logging.info(f"You choosed: {filePath}, packing...")
        if os.path.isfile(filePath + "/index.html") or os.path.isfile(filePath + "/index.htm"): # type: ignore
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
    else:
        if filePath.split('.')[-1] == 'bs9':
            logging.info(f"You choosed: {filePath}, decoding...")
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
        elif filePath.split('.')[-1] == 'bs9pck':
            logging.info(f"You choosed: {filePath}, unpacking...")
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
        elif filePath.split('.')[-1] == 'txt':
            logging.info(f"You choosed: {filePath}, encoding...")
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
        else:
            logging.critical('Invalid target file...')
            sys.exit(1)

if __name__ == "__main__":
    main()