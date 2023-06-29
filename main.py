""" Temporary Main file for testing

"""

from src.scraper import Scraper
from src.database import Database


def main():
    isbn = Scraper.parse_isbn("143039431")
    book_stats = Scraper.fetch_book_stats(isbn)
    print(book_stats)

    DB = Database()
    DB.update_book_prices()


if __name__ == "__main__":
    main()
