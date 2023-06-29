""" This performs all SQL queries. 
    such as but not limited to, adding users, books, wishlists,
    removing, and more.
"""

from configparser import ConfigParser
import psycopg2

# TODO Change to a config file before commiting

class Database:

    # constants for connecting
    config = ConfigParser()
    config.read("config/server_config.ini")
    

    conn = None
    cursor = None

    # Opens connections to SQL Database. Must be called for every update funciton.
    def open_connection(self):
        try:
            self.conn = psycopg2.connect(
                        host = self.config['server']['hostname'],
                        dbname = self.config['server']['database'],
                        user = self.config['server']['username'],
                        password = self.config['server']['pwd'],
                        port = self.config['server']['port_id'])

            self.cursor = self.conn.cursor()

        except Exception as error:
            print(error)
            if self.cursor is not None:
                self.cursor.close()

            if self.conn is not None:
                self.conn.close()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def add_book(self, stats):

        update_book_script  = "INSERT INTO public.\"Book\" (title, isbn10, amazon_price, author) VALUES (%s, %s, %s, %s)"
        
        self.open_connection()

        self.cursor.execute(update_book_script, stats)
        
        self.conn.commit()

        self.close_connection()


