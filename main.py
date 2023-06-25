from scraper import Book


def main():
    print("Enter the ISBN you'd like to search: ")
    isbn = input()
    isbn = Book.parse_isbn(isbn)
    book_stats = Book.fetch_amazon_stats(isbn)
    print(book_stats)


if __name__ == "__main__":
    main()
