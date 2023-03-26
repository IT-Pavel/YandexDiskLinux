import sys
from enum import Enum, IntEnum
from typing import *

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt, QModelIndex, QAbstractItemModel, QAbstractTableModel

if __name__ == "__main__":
    print("This is a module")
    sys.exit()


class FileType(IntEnum):
    Unknown = 0
    Folder = 1
    Link = 2
    File = 4


class FileInfo:
    Name: str = ""
    Path: str = ""
    Type:FileType = FileType.Unknown
    IsSynchronyze: bool = True
    IsSynchronyzed: bool = False

    def __str__(self) -> str:
        res_str: str = f"FileInfo object: "
        res_str += f"Name:{self.Name}, "
        res_str += f"Path:{self.Path}, "
        res_str += f"IsDir:{self.IsDir}, "
        res_str += f"IsLink:{self.IsLink}, "
        res_str += f"IsFile:{self.IsFile}, "
        res_str += f"IsSynchronyze:{self.IsSynchronyze}, "
        res_str += f"IsSynchronyzed:{self.IsSynchronyzed}\n"
        return res_str

    def __repr__(self) -> str:
        return self.__str__()


