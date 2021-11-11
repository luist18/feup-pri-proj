class Book:
    def __init__(self, name, url, id, session):
        self.name = name
        self.url = url
        self.id = id
        self.session = session

    def __repr__(self):
        return f"<Book {self.name}, {len(self.url)}>"
