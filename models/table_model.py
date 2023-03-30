from PyQt6 import QtGui
from PyQt6.QtCore import QAbstractTableModel, Qt

from .file_model import FileType
class FileTableModel(QAbstractTableModel):
    def __init__(self, data, headers) -> None:
        super(FileTableModel, self).__init__()
        self._data = data
        self._headers = headers

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, bool):
                if index.column()==2:
                    if value:
                        return 'Вкл.'
                    return 'Выкл.'
            return value

        if role == Qt.ItemDataRole.DecorationRole:
            value = self._data[index.row()][index.column()]
            if index.column()==2:
                if isinstance(value, bool):
                    if value:
                        return QtGui.QIcon('./icons/tick.png')
                    return QtGui.QIcon('./icons/cross.png')
            if index.column()==0:
                if isinstance(value,int):
                    if value == FileType.Folder:
                        return QtGui.QIcon('./icons/folder_stand.png')
                    return QtGui.QIcon('./icons/newspaper.png')

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if index.column() == 2:
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignHCenter

    def rowCount(self, index) -> int:
        return len(self._data)

    def columnCount(self, index) -> int:
        if len(self._data)==0:
            return 0
        return len(self._data[0])

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
            # if orientation == Qt.Orientation.Vertical:
            #     return section+1