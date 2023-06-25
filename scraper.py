""" This is the webscraping module for the upcoming Project Wishy.
    Jerrod Pope May 4 2022

    Most of this is test code to instantiate a proof of concept. This file will
    be responsible for scraping various booksellers for price as well as
    fetching book stats from Amzaon. Later functionality will include adding
    new books to a database for website implementation.

    Required Libraries:
        bs4 - Beautiful Soup 4 for web scraping
        requests - Acquiring html data from web
        pyisbn - ISBN handling
        lxml - HTML Parser

    *TO-DO:
        - implement exception handling
        - add Barnes & Noble price scraping
        - implement test SQLite3 database before using PostgreSQL
        - update sqlite3 database info from Amazon in constructor

    """
from bs4 import BeautifulSoup
import requests
import pyisbn

# Necessary header for HTTP 200 response code.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://google.com",
    "Dnt": "1",
}

# CONSTANTS
AMAZON_URL = "https://www.amazon.com/s?k="


class Book:
    """Test class for book. Plans to imporve this class are in the to-do list
    at the top
    """

    @staticmethod
    def parse_isbn(isbn):
        """
        Determines validity of an ISBN-10 or ISBN-13 then converts to
        ISBN-10, for Amazon searching

        Args:
            isbn (string): target isbn for validating and converting to ISBN-10

        Returns:
            string: validated and converted ISBN-10
        """

        if not pyisbn.validate(isbn):
            return "Invalid ISBN"

        # Convert unkown ISBN type to ISBN10 for Amazon
        validated_isbn10 = pyisbn.convert(isbn)

        return validated_isbn10

    # Get multiple URL sites mostly using the pyisbn API
    @staticmethod
    def get_google_url(validated_isbn10):
        """Return google URL for book given a validated ISBN-10

        Args:
            validated_isbn10 (string): ISBN-10 Validaed with "Book.parse()"

        Returns:
            string: Google URL for ISBN provided.
        """
        book = pyisbn.Isbn(validated_isbn10)
        return book.to_url("google", "us")

    @staticmethod
    def fetch_amazon_stats(validated_isbn10):
        """Get Amazon Stats for book. Will later be updated to initialize a
        database entry

        Args:
            validated_isbn10 (string): ISBN-10 Validaed with "Book.parse()"

        Returns:
            list: [
                string: title,
                string: validated_isbn10,
                float: price,
                atring: author
            ]
        """

        html_http_response = requests.get(
            AMAZON_URL + validated_isbn10, headers=HEADERS
        )

        # Ensure a proper HTTP response of 200
        if str(html_http_response) != "<Response [200]>":
            return [None]

        html_text = html_http_response.text

        # Parse html data using lxml parser library
        soup = BeautifulSoup(html_text, "lxml")
        title_card = soup.find("div", {"data-asin": validated_isbn10})

        # Heading <h2> will return the product title.
        # price and author are less intuitive
        title = title_card.find("h2").text
        price = title_card.find("span", {"class": "a-offscreen"}).text
        author = title_card.find(
            "a",
            {
                "class": "a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style"
            },
        ).text

        title = title.strip()  # Strip whitespace from title and author
        author = author.strip()
        price = float(price.replace("$", ""))

        book_info = [title, validated_isbn10, price, author]
        return book_info

    @staticmethod
    def fetch_amazon_price(validated_isbn10):
        """Returns amazon price for book given a validated ISBN-10

        Args:
            validated_isbn10 (string): ISBN-10 validated with "Book.parse()"

        Returns:
            float: price of book on Amazon
        """
        html_http_response = requests.get(
            AMAZON_URL + validated_isbn10, headers=HEADERS
        )

        if str(html_http_response) != "<Response [200]>":
            return [None]  # TODO Needs proper error handling

        html_text = html_http_response.text

        # Parse html data using lxml parser library
        soup = BeautifulSoup(html_text, "lxml")

        # Named "title_card" because i'm unsure of proper HTML or CSS name.
        title_card = soup.find("div", {"data-asin": validated_isbn10})

        price = title_card.find("span", {"class": "a-offscreen"}).text

        return float(price.replace("$", ""))
