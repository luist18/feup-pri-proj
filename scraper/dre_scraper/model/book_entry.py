from enum import Enum


class BookEntryType(Enum):
    ARTICLE = 1
    SECTION = 2


class BookEntry():

    def __init__(self, name, type, depth=0, url=None):
        self.name = name
        self.type = type
        self.depth = depth
        self.url = url

    def __repr__(self):
        return f"<BookEntry {self.name}, {self.type} type, {self.depth} depth, {self.url}>"
