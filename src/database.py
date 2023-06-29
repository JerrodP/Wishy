""" This performs all SQL queries. 
    such as but not limited to, adding users, books, wishlists,
    removing, and more.
"""

from configparser import ConfigParser
import psycopg2


class Database:
    """
    Database class is used to perform all actions on the database.
    Ensure proper exceptions are handled or connections won't be closed and
    will remain open to the database server.
    """

    # constants for connecting
    config = ConfigParser()
    config.read("config/server_config.ini")

    conn = None
    cursor = None

    # Destructor
    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def open_connection(self):
        """# Opens connections to SQL Database. Must be called before every update funciton."""
        try:
            self.conn = psycopg2.connect(
                host=self.config["server"]["hostname"],
                dbname=self.config["server"]["database"],
                user=self.config["server"]["username"],
                password=self.config["server"]["pwd"],
                port=self.config["server"]["port_id"],
            )

            self.cursor = self.conn.cursor()

        except psycopg2.OperationalError as error:
            print(error)
            if self.cursor is not None:
                self.cursor.close()

            if self.conn is not None:
                self.conn.close()

    def close_connection(self):
        """Closes connections to SQL Database. Must be called after every update funciton."""
        self.cursor.close()
        self.conn.close()

    def add_new_book(self, stats):
        """Adds a new book to database."""
        add_book_script = "INSERT INTO public.Book (title, isbn10, amazon_price, author) VALUES (%s, %s, %s, %s)"

        self.open_connection()

        try:
            self.cursor.execute(add_book_script, stats)
        except psycopg2.IntegrityError:
            self.conn.rollback()
        else:
            self.conn.commit()
        finally:
            self.close_connection()

    def add_new_user(self, user_list):
        """Adds a new user to the database. where user_lsit is :
        ['first_name', 'last_name', 'email_address']
        """

        add_user_script = "INSERT INTO public.Wishy_User (first_name, last_name, email) VALUES (%s, %s, %s)"

        user_list[2] = user_list[2].lower()

        self.open_connection()

        try:
            self.cursor.execute(add_user_script, user_list)
        except psycopg2.IntegrityError:
            self.conn.rollback()
        else:
            self.conn.commit()
        finally:
            self.close_connection()

    def add_book_to_wishlist(self, user_list, book_stats):
        """Adds book and user to wishlist table.
        Also checks to make sure there's no duplicates."""

        user_email = user_list[2].lower()
        validated_isbn = book_stats[1]

        self.add_new_book(book_stats)
        self.add_new_user(user_list)

        add_wishlist_script = (
            "INSERT INTO public.wishlist (email, isbn10) VALUES ('%s', %s)"
            % (user_email, validated_isbn)
        )

        self.open_connection()

        try:
            self.cursor.execute(add_wishlist_script)
        except psycopg2.IntegrityError:
            self.conn.rollback()
        else:
            self.conn.commit()
        finally:
            self.close_connection()

    def get_user_wishlist(self, user_email):
        """Get user wishlist from database."""

        get_user_wishlist_script = str(
            """SELECT u.first_name, u.last_name, w.isbn10
            from public.wishy_user u
            inner join wishlist w
            on u.email = w.email
            where u.email = '%s';"""
            % user_email
        )

        self.open_connection()

        try:
            self.cursor.execute(get_user_wishlist_script)
            records = self.cursor.fetchall()
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            self.close_connection()

        return records
