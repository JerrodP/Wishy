# Wishy

## A Project for helping me save money on books

The Wishy program's goal is to scrape data from Amazon to get prices and notify users when the price changes. The user will need to provide an IBSN or an ASIN and the rest should be handled, from getting book information to notifying the user of a price change.

## Goal
The goal of this project is to accomplish 
the following tasks to improve my programming skills and familiarity with Python, Docker, SQL, and more.

1. Follow a consistent design pattern
2. Better understand how Python interacts with outside databases.
3. Integrate a normalized SQL database with CRUD functionality to maintain a database of books.
4. Learn how to run this system on a Raspberry Pi using Docker.

## Further design ideas:
1. Setup virtual machine or server to have program running at all times to update users more consistently
2. Implement user authentification
3. Develop webapp or app interface.
4. Edit class structure to add more than just books, ie any Amazon product.


## Installation
1. Setup a virtual env:
    `python -m venv wishy_env`
2. run the activate.bat in wishy_env\scripts
3. Install proper packages using: `pip install -r requirents.txt`
4. Restart language server and Black if necessary.
