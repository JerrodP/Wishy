""" Temporary Main file for testing

"""

from src.scraper import Scraper
from src.database import Database


def main():
    isbn = "978-1635575552"
    # isbn = "0143039431"
    isbn = Scraper.parse_isbn(isbn)
    book_stats = Scraper.fetch_amazon_stats(isbn)
    print(book_stats)
    DB = Database()
    DB.add_book(book_stats)


if __name__ == "__main__":
    main()
