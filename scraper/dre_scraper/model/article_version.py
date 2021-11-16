class ArticleVersion():

    def __init__(self, text, details=None, initial=False):
        self.text = text
        self.details = details
        self.initial = initial

    def __repr__(self):
        return f"<Change {self.details}, {self.initial}, {self.text}>"
