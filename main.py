import os
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem

from models.file_model import FileInfo, FileType
from models.file_tree_model import FileTreeModel
from models.table_model import FileTableModel
from windows.main_window import Ui_MainWindow

YaDiskPath: str = '/home/it-pavel/Yandex.Disk'

fileList: list = list()

table_headers = ['', 'Имя', 'Синхр.'] 

ui: Ui_MainWindow = None


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
    fileList.sort(key=lambda x: x.Type)

    dirList = list()
    for item in fileList:
        if item.Type == FileType.Folder:
            dirList.append(item)

    dataTable: list = list()
    dataTree: list = list()
    
    # item:FileInfo
    for item in fileList:
        dataTable.append([
            item.Type,
            item.Name,
            item.IsSynchronyze])
        if item.Type == FileType.Folder:
            dataTree.append(item)

    tableModel = FileTableModel(dataTable, table_headers)
    ui.fileTable.setModel(tableModel)
    items = []
    item = QTreeWidgetItem(["Yandex.Disk"])
    item.addChild(QTreeWidgetItem(['']))
    items.append(item)
    ui.fileTree.setColumnCount(1)
    ui.fileTree.insertTopLevelItems(0, items.copy())
    ui.fileTree.topLevelItem(0).setExpanded(True)


def ConfigureUi() -> None:
    pass


def ReadSettings():
    pass


def fileTreeExpanded(item: QTreeWidgetItem):

    currentPath: str = buildPath(item)

    ls_res = os.listdir(currentPath)
    folderList: list = []
    for item_res in ls_res:
        if item_res.find('.') != -1:
            continue
        if os.path.isdir(f"{currentPath}/{item_res}"):
            folderList.append(item_res)
    folderList.sort()
    child: QTreeWidgetItem = None

    while item.childCount() > 0:
        child = item.child(0)
        item.removeChild(child)

    for folder in folderList:
        newItem = QTreeWidgetItem([folder])
        newItem.addChild(QTreeWidgetItem(['']))
        item.addChild(newItem)


def fileTreeItemCliked(item: QTreeWidgetItem):
    currentPath:str = buildPath(item)
    fillFileTable(currentPath)

def buildPath(item: QTreeWidgetItem) -> str:
    folderList: list = list()
    folderList.append(item.data(0, Qt.ItemDataRole.DisplayRole))
    parent: QTreeWidgetItem = item.parent()
    while parent != None:
        folderList.append(parent.data(0, Qt.ItemDataRole.DisplayRole))
        parent = parent.parent()

    folderList.pop()
    folderList.reverse()
    currentPath: str = YaDiskPath
    for folder in folderList:
        currentPath += f"/{folder}"
    return currentPath

def fillFileTable(path:str)->None:
    ls_res = os.listdir(path)
    fileList:list = []
    for ls_item in ls_res:
        fileItem:FileInfo = FileInfo()
        fileItem.Name = ls_item
        fileItem.Path = f'{path}/{ls_item}'
        
        if os.path.isdir(fileItem.Path):
            fileItem.Type = FileType.Folder
        if os.path.isfile(fileItem.Path):
            fileItem.Type = FileType.File
        if os.path.islink(fileItem.Path):
            fileItem.Type = FileType.Link
        fileList.append(fileItem)
    
    fileList.sort(key=lambda x: x.Path)
    fileList.sort(key=lambda x: x.Type)
    
    dataTable: list = []
    item:FileInfo
    for item in fileList:
        dataTable.append([
            item.Type,
            item.Name,
            item.IsSynchronyze])
    
    tableModel:FileTableModel = FileTableModel(dataTable,table_headers)
    ui.fileTable.setModel(tableModel)

def main():
    global ui
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    ConfigureUi()

    window.show()

    # Connect events
    ui.fileTree.itemExpanded.connect(fileTreeExpanded)
    ui.fileTree.itemClicked.connect(fileTreeItemCliked)

    OnLoad()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
