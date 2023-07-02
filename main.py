""" Temporary Main file for testing

"""

from src.scraper import Scraper
from src.database import Database


def main():
    Scrape = Scraper()
    isbn = Scrape.parse_isbn("143039431")
    book_stats = Scrape.fetch_book_stats(isbn)
    print(book_stats)



if __name__ == "__main__":
    main()
