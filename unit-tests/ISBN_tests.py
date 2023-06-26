import unittest
from scraper import Book


class ISBNTests(unittest.TestCase):

    def test_isbn_10(self):
        isbn = "0241265541"
        isbn = Book.parse_isbn(isbn)
        stats = Book.fetch_amazon_stats(isbn)

        title = "War and Peace (Penguin Clothbound Classics)"
        author = "Leo Tolstoy"

        self.assertEqual(stats[0], title)
        self.assertEqual(stats[3], author)

    def test_isbn_13(self):
        isbn = "9780486415871"
        isbn = Book.parse_isbn(isbn)
        stats = Book.fetch_amazon_stats(isbn)

        title = "Crime and Punishment (Dover Thrift Editions: Classic Novels)"
        author = "Fyodor Dostoyevsky"

        self.assertEqual(stats[0], title)
        self.assertEqual(stats[3], author)

    def test_parsing(self):
        isbn = "9-7-8-0-4-8-6-4-1-5-8-7-1     "
        isbn = Book.parse_isbn(isbn)
        self.assertEqual(isbn, "0486415872")

if __name__ == '__main__':
    unittest.main()
