""" This is the webscraping module for the upcoming Project Wishy.
    Jerrod Pope May 4 2022

    Most of this is test code to instantiate a proof of concept. This file will
    be responsible for scraping various booksellers for price as well as
    fetching book stats from Amzaon. Later functionality will include adding
    new books to a database for website implementation.

    """
from bs4 import BeautifulSoup
from configparser import ConfigParser
import requests
import pyisbn
import sys

# Appending system path because loading Python modules is the stupidiest...
from os.path import dirname, abspath
d = dirname(dirname(__file__))
sys.path.append(d)

import src.headers as Headers


# Necessary header for HTTP 200 response code.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://google.com",
    "Dnt": "1",
}

# CONSTANTS
AMAZON_URL = "https://www.amazon.com/s?k="

class Scraper:
    """
    Test class for book. Plans to imporve this class are in the to-do list
    at the top
    """

    PROXIES = None
    fingerprint = None

    def __init__(self):
        # Proxy server connection
        config = ConfigParser()
        config.read("config/server_config.ini")
        USERNAME = config['proxy']['username']
        PASSWORD = config['proxy']['password']
        # self.fingerprint = Headers.get_fingerprint()

        self.PROXIES = {
            'http': 'http://customer-%s-cc-us-st-us_alabama-sessid-0768333109-sesstime-10:%s@pr.oxylabs.io:7777' % (USERNAME, PASSWORD),   
            'https': 'https://customer-%s-cc-us-st-us_alabama-sessid-0768333109-sesstime-10:%s@pr.oxylabs.io:7777' % (USERNAME, PASSWORD)
        }


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

        # strip all non-numerical characters from input
        temp = ""
        for c in isbn:
            if c.isdigit():
                temp = temp + c
        isbn = temp

        # Ensure appropriate isbn length
        isbn = isbn.zfill(10)

        if not pyisbn.validate(isbn):
            return "Invalid ISBN"

        # Convert unkown ISBN type to ISBN10 for Amazon
        if len(isbn) == 10:
            return isbn
        else:
            return pyisbn.convert(isbn, "978")

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

    def fetch_book_stats(self, validated_isbn10):
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
            AMAZON_URL + validated_isbn10,
            headers=Headers.get_fingerprint(),
            proxies=self.PROXIES,
            timeout=3
        )

        # TODO remove, needed for testing only
        print("Size of Amazon request: ", len(html_http_response.content))

        # Ensure a proper HTTP response of 200
        if str(html_http_response) == "<Response [503]>":
            print("Response 503 received")
            return None

        if str(html_http_response) != "<Response [200]>":
            return None

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
    def fetch_amazon_price(self, validated_isbn10):
        """Returns amazon price for book given a validated ISBN-10

        Args:
            validated_isbn10 (string): ISBN-10 validated with "Book.parse()"

        Returns:
            float: price of book on Amazon
        """
        html_http_response = requests.get(
            AMAZON_URL + str(validated_isbn10),
            headers=Headers.get_fingerprint(),
            proxies=self.PROXIES,
            timeout=3

        )

        if str(html_http_response) != "<Response [200]>":
            return [None]  # TODO Needs proper error handling

        html_text = html_http_response.text

        # Parse html data using lxml parser library
        soup = BeautifulSoup(html_text, "lxml")

        # Named "title_card" because i'm unsure of proper HTML or CSS name.
        title_card = soup.find("div", {"data-asin": validated_isbn10})

        price_card = title_card.find("span", {"class": "a-price"})
        price = price_card.find("span", {"class": "a-offscreen"}).text

        return float(price.replace("$", ""))
