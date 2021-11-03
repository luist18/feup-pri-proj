class Book:
    def __init__(self, name, articles):
        self.name = name
        self.articles = articles

    def __repr__(self):
        return f"<Book {self.name}, {len(self.articles)} articles>"
