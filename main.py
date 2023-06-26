from scraper import Book


def main():
    isbn = "978-0143039433"
    # isbn = "0143039431"
    isbn = Book.parse_isbn(isbn)
    book_stats = Book.fetch_amazon_stats(isbn)
    print(book_stats)


if __name__ == "__main__":
    main()
