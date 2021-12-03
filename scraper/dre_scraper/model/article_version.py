class ArticleVersion():

    id = 1

    def __init__(self, title, text, details=None, initial=False):
        self.title = title
        self.text = text
        self.details = details
        self.initial = initial

        # Set id and increment it
        self.id = ArticleVersion.id
        ArticleVersion.id += 1

    def __repr__(self):
        return f"<Change {self.title} {self.details}, {self.initial}, {self.text}>"
