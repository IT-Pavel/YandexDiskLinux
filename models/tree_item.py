class TreeItem():
    def __init__(self, data: list, parent: 'TreeItem' = None):
        self.__item_data = data
        self.__parent = parent
        self.__child_items = []

    def child(self, number: int) -> 'TreeItem':
        if number < 0 or number >= len(self.__child_items):
            return None
        return self.__child_items[number]

    def last_child(self):
        return self.__child_items[-1] if self.__child_items else None

    def child_count(self) -> int:
        return len(self.__child_items)

    def child_number(self) -> int:
        return self.__parent.__child_items.index(self)

    def column_count(self) -> int:
        return len(self.__item_data)

    def data(self, colunm: int):
        if colunm < 0 or colunm >= len(self.__item_data):
            return None
        return self.__item_data[colunm]

    def insert_children(self, position: int, count: int, columns: int) -> bool:
        if position < 0 or position > len(self.__child_items):
            return False

        for row in range(count):
            data = [None] * columns
            item = TreeItem(data.copy(), self)
            self.__child_items.insert(position, item)

        return True

    def insert_colunms(self, position: int, columns: int) -> bool:
        if position < 0 or position > len(self.__item_data):
            return False

        for column in range(columns):
            self.__item_data.insert(position, None)
        for child in self.__child_items:
            child.insert_columns(position, columns)

        return True

    def parent(self):
        return self.__parent

    def remove_children(self, position: int, count: int) -> bool:
        if position < 0 or position + count > len(self.__child_items):
            return False
        for row in range(count):
            self.__child_items.pop(position)

        return True

    def remove_colunms(self, position: int, colunms: int) -> bool:
        if position < 0 or position + colunms > len(self.__item_data):
            return False
        for colunm in range(colunms):
            self.__item_data.pop(position)

        for child in self.__child_items:
            self.remove_colunms(position, colunms)

        return True

    def set_data(self, colunm: int, value) -> bool:
        if colunm < 0 or colunm >= len(self.__item_data):
            return False
        self.__item_data[colunm] = value
        return True

    def __str__(self) -> str:
        result = f"<treeitem.TreeItem at 0x{id(self):x}"
        result += f' "{self.__item_data}"' if self.__item_data else " <None>"
        result += f", {len(self.__child_items)} children>"
        return result

    def __repr__(self) -> str:
        return self.__str__()
