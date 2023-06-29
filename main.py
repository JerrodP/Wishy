""" Temporary Main file for testing

"""

from src.scraper import Scraper
from src.database import Database


def main():
    DB = Database()

    isbn = "978-1400079278"
    # isbn = "0143039431"
    isbn = Scraper.parse_isbn(isbn)
    book_stats = Scraper.fetch_book_stats(isbn)
    print(book_stats)
    DB.add_new_book(book_stats)


if __name__ == "__main__":
    main()
