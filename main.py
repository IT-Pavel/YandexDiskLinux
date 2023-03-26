import os
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow

from models.file_model import FileInfo, FileType
from models.table_model import FileTableModel
from windows.main_window import Ui_MainWindow

YaDiskPath: str = '/home/it-pavel/Yandex.Disk'

fileList: list = list()

currentDir:str = YaDiskPath

ui:Ui_MainWindow = None       
        
def OnLoad():
    ls_res = os.listdir(YaDiskPath)
    for item in ls_res:
        if item[0] == ".":
            continue
        fileItem: FileInfo = FileInfo()
        fileItem.Name = item
        fileItem.Path = f"{YaDiskPath}/{item}"
        if os.path.isfile(fileItem.Path):
            fileItem.Type = FileType.File
        if os.path.isdir(fileItem.Path):
            fileItem.Type = FileType.Folder
        if os.path.islink(fileItem.Path):
            fileItem.FileType = FileType.Link
        fileList.append(fileItem)
    
    fileList.sort(key=lambda x: x.Path) 
    fileList.sort(key= lambda x: x.Type)
    
    dirList = list()
    for item in fileList:
        if item.Type==FileType.Folder:
            dirList.append(item)
    
    dataTable:list = list()
    dataTree:list = list()
    headers = ['','Имя','Синхр.']
    # item:FileInfo
    for item in fileList:
        dataTable.append([
            item.Type,
            item.Name,
            item.IsSynchronyze])
        if item.Type == FileType.Folder:
            dataTree.append(item.Name)
    
    tableModel = FileTableModel(dataTable,['','Name','Sync'])
    ui.fileTable.setModel(tableModel)
    
        
def ConfigureUi()->None:
    pass

def ReadSettings():
    pass


def main():
    global ui
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    ConfigureUi()

    window.show()

    OnLoad()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
