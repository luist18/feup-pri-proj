class Legislation:
    def __init__(self, books):
        self.books = books

    def __repr__(self):
        return f"<Legislation {len(self.books)} books>"
