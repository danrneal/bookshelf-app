"""Test objects used to test the behavior of endpoints in the flaskr app"""

import unittest
from flask_sqlalchemy import SQLAlchemy
from flaskr import app
from models import DB_DIALECT, DB_HOST, DB_PORT, setup_db, Book


class BookTestCase(unittest.TestCase):
    """This class represents the test cases for the book endpoints

    Attributes:
        app: A flask app from the flaskr app
        client: A test client for the flask app to while testing
        db_name: A str representing the name of the test database
        db_path: A str representing the location of the test database
        new_book: A dict representing a new book to use in tests
    """

    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.db_name = 'bookshelf_test'
        self.db_path = f'{DB_DIALECT}://{DB_HOST}:{DB_PORT}/{self.db_name}'
        setup_db(self.app, self.db_path)

        self.new_book = {
            'title': 'Anansi Boys',
            'author': 'Neil Gaiman',
            'rating': 5
        }

    def tearDown(self):
        """Executed after each test"""


# @TODO: Write at least two tests for each endpoint - one each for success and
#           error behavior.
#        You can feel free to write additional tests for nuanced functionality,
#        Such as adding a book without a rating, etc.
#        Since there are four routes currently, you should have at least eight
#           tests.
# Optional: Update the book information in setUp to make the test database
#           your own!


if __name__ == "__main__":
    unittest.main()
