from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QModelIndex, QAbstractItemModel
from .tree_item import TreeItem


class FileTreeModel(QAbstractItemModel):
    def __init__(self, headers: list, data: list, parent) -> None:
        super().__init__(parent)

        self.__root_data = headers
        self.__root_item = TreeItem(self.__root_data.copy())
        self.setup_model_data(data,self.__root_item)

    def columnCount(self, parent: QModelIndex = None) -> int:
        return self.__root_item.column_count()

    def data(self, index: QModelIndex, role: int = None):
        if not index.isValid():
            return None
        if role != Qt.ItemDataRole.DisplayRole and role != Qt.ItemDataRole.EditRole:
            return None
        item: TreeItem = self.get_item(index)
        return item.data(index.column())

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsEditable | QAbstractItemModel.flags(self, index)

    def get_item(self, index: QModelIndex = QModelIndex()) -> TreeItem:
        if index.isValid():
            item: TreeItem = index.internalPointer()
            if item:
                return item
        return self.__root_item

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.__root_item.data(section)
        return None

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        if parent.isValid() and parent.column != 0:
            return QModelIndex()
        parent_item: TreeItem = self.get_item(parent)
        if not parent_item:
            return QModelIndex()
        child_item: TreeItem = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QModelIndex()

    def insertColumns(self, position: int, colunms: int, parent: QModelIndex = QModelIndex()) -> bool:
        self.beginInsertColumns(parent, position, position+colunms-1)
        success: bool = self.__root_item.insert_colunms(position, colunms)
        self.endInsertColumns()
        return success

    def insertRows(self, position: int, rows: int, parent: QModelIndex = QModelIndex()) -> bool:
        parent_item: TreeItem = self.get_item(parent)
        if not parent_item:
            return False

        self.beginInsertColumns(parent, position, position+rows-1)
        column_count = self.__root_item.column_count()
        success: bool = parent_item.insert_children(
            position, rows, column_count)
        self.endInsertRows
        return success

    def parent(self, index: QModelIndex = QModelIndex()) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()

        child_item: TreeItem = self.get_item(index)
        if child_item:
            parent_item: TreeItem = child_item.parent()
        else:
            parent_item = None

        if parent_item == self.__root_item or not parent_item:
            return QModelIndex()
        return self.createIndex(parent_item.child_number(), 0, parent_item)

    def removeColumns(self, position: int, columns: int, parent: QModelIndex = QModelIndex()) -> bool:
        self.beginRemoveColumns(parent, position, position+columns-1)
        success: bool = self.__root_item.remove_colunms(position, columns)
        self.endRemoveColumns()

        if self.__root_item.column_count == 0:
            self.removeRows(0, self.rowCount())

        return success

    def removeRows(self, position: int, rows: int, parent: QModelIndex = QModelIndex()) -> bool:
        parent_item: TreeItem = self.get_item(parent)
        if not parent_item:
            return False

        self.beginRemoveRows(parent, position, position+rows-1)
        success: bool = parent_item.remove_children(position, rows)
        self.endRemoveRows

        return success

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid() and parent.column() > 0:
            return 0
        parent_item: TreeItem = self.get_item(parent)
        if not parent_item:
            return 0
        return parent_item.child_count()

    def setData(self, index: QModelIndex, value, role: int) -> bool:
        if role != Qt.ItemDataRole.EditRole:
            return False

        item: TreeItem = self.get_item(index)
        success: bool = item.set_data(index.column(), value)

        if success:
            self.dataChanged.emit(index, index,
                                  [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
        return success

    def setHeaderData(self, section: int, orientation: Qt.Orientation, value, role: int = None) -> bool:
        if role != Qt.ItemDataRole.EditRole or orientation != Qt.Orientation.Horizontal:
            return False

        success: bool = self.__root_item.set_data(section, value)
        if success:
            self.headerDataChanged.emit(orientation, section, section)
        return success

    def __repr_recursion(self, item: TreeItem, indent: int = 0) -> str:
        result = " " * indent + repr(item) + "\n"
        for index in range(item.child_count()):
            result += self.__repr_recursion(item.child(index), indent + 2)
        return result

    def __repr__(self) -> str:
        return self.__repr_recursion(self.__root_item)

    def __str__(self) -> str:
        return self.__repr__()

    def setup_model_data(self, lines: list, parent: TreeItem):
        for line in lines:
            success:bool = parent.insert_children(parent.child_count(),1,len(line))
            # if not success:
            #     print(line)
            #     continue
            
            for index,column in enumerate(line):
                child:TreeItem = parent.last_child()
                child.set_data(index,column)
                child.insert_children(0,1,len(line))
            