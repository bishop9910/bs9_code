#bs9FileInfoReader
#python -m nuitka --onefile --show-memory --show-progress --enable-plugin=pyside6 --remove-output --windows-icon-from-ico=./bs9FileInfoReader.ico bs9FileInfoReader.py
from PySide6.QtWidgets import QApplication, QFileDialog
from header import read_header
import sys
import os

if __name__ == '__main__':
    app = QApplication([])
    if len(sys.argv) != 1:
        if os.path.isfile(sys.argv[1]):
            filePath = sys.argv[1]
        else:
            filePath, _ = QFileDialog.getOpenFileName(None,"Select the file",'',"bishop9910 files (*.bs9);;bishop9910 package files (*.bs9pck);;All files (*)")
    else:
        filePath, _ = QFileDialog.getOpenFileName(None,"Select the file",'',"bishop9910 files (*.bs9);;bishop9910 package files (*.bs9pck);;All files (*)")

    if filePath == '' or filePath == None:
        print('Error: Not select a file.')
        sys.exit(1)
    header = read_header(filePath)
    info = header.decode('utf-8').split('_')
    fileType = info[0]
    readedVersion = f'v{info[1]}'
    convert_ID = f'{info[2]}(hex)'
    convert_code = str(int(info[2], 16)//5891)
    print(f"{fileType=}\n{readedVersion=}\n{convert_ID=}\n{convert_code=}")
    input()