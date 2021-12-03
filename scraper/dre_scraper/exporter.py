import csv
import os


def export_to_csv(legislation):
    """
    Export the legislation to a CSV file.
    """

    # book.csv - id, name, url, root_section
    # section.csv - id, name, depth, parent (can be None)
    # article.csv - id, section, title, header, state, text
    # article_version.csv - id, article_id, text, details (can be None), initial

    books_file = open("./book.csv", "w", newline="", encoding="utf-8")
    books_writer = csv.writer(books_file)
    books_writer.writerow(["id", "name", "url", "root_section_id"])

    sections_file = open("./section.csv", "w", newline="", encoding="utf-8")
    sections_writer = csv.writer(sections_file)
    sections_writer.writerow(["id", "name", "depth", "parent_id"])

    articles_file = open("./article.csv", "w", newline="", encoding="utf-8")
    articles_writer = csv.writer(articles_file)
    articles_writer.writerow(
        ["id", "section_id", "title", "header", "state", "text"])

    articles_versions_file = open(
        "./article_version.csv", "w", newline="", encoding="utf-8")
    articles_versions_writer = csv.writer(articles_versions_file)
    articles_versions_writer.writerow(
        ["id", "article_id", "title", "text", "details", "initial"])

    for book in legislation.books:
        books_writer.writerow(
            [book.id, book.name, book.url, book.root_section.id])

        __export_sections_to_csv(
            book.root_section, sections_writer, articles_writer, articles_versions_writer)

    books_file.close()
    sections_file.close()
    articles_file.close()
    articles_versions_file.close()


def __export_sections_to_csv(current_section, sections_writer, articles_writer, articles_versions_writer):
    """
    Export the sections to a CSV file.
    """

    sections_writer.writerow(
        [current_section.id, current_section.name, current_section.depth, current_section.parent.id if current_section.parent else None])

    for section in current_section.sections:
        __export_sections_to_csv(
            section, sections_writer, articles_writer, articles_versions_writer)

    for article in current_section.articles:
        articles_writer.writerow(
            [article.id, current_section.id, article.title, article.header, article.state, article.text])

        for version in article.versions:
            articles_versions_writer.writerow(
                [version.id, article.id, version.title, version.text, version.details, version.initial])
