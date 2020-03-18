"""Test objects used to test the behavior of endpoints in the flaskr app"""

import unittest
from flaskr import BOOKS_PER_SHELF, app
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

    def test_create_book_success(self):
        """Test successful creation of a book"""

        response = self.client().post('/books', json=self.new_book)
        created_book_id = response.json.get('created_book_id')
        book = Book.query.get(created_book_id)
        self.new_book['id'] = created_book_id

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json.get('success'))
        self.assertTrue(response.json.get('books'))
        self.assertTrue(response.json.get('total_books'))
        self.assertEqual(book.format(), self.new_book)

    def test_create_book_no_info_fail(self):
        """Test failed book creation when no book info is present"""

        response = self.client().post('/books')

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json.get('success'))
        self.assertEqual(response.json.get('message'), 'Bad Request')

    def test_get_books_success(self):
        """Test successful retrieval of books"""

        response = self.client().post('/books', json=self.new_book)
        response = self.client().get('books')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json.get('success'))
        self.assertTrue(response.json.get('books'))
        self.assertTrue(response.json.get('total_books'))

    def test_get_books_out_of_range_fail(self):
        """Test failed book retrieval when page number is out of range"""

        response = self.client().post('/books', json=self.new_book)
        total_books = response.json.get('total_books')
        total_pages = -(-total_books // BOOKS_PER_SHELF)
        response = self.client().get(f'/books?page={total_pages+1}')

        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json.get('success'))
        self.assertEqual(response.json.get('message'), 'Not Found')

    def test_search_books_success(self):
        """Test successful of search of books"""

        response = self.client().post('/books', json=self.new_book)
        response = self.client().post('/books', json={'search': 'boys'})

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json.get('created_book_id'))
        self.assertTrue(response.json.get('success'))
        self.assertTrue(response.json.get('books'))
        self.assertGreater(response.json.get('total_books'), 0)

    def test_search_books_no_results(self):
        """Test a search of books that returned no results"""

        response = self.client().post('/books', json=self.new_book)
        response = self.client().post('/books', json={'search': 'girls'})

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json.get('created_book_id'))
        self.assertTrue(response.json.get('success'))
        self.assertEqual(response.json.get('books'), [])
        self.assertEqual(response.json.get('total_books'), 0)

    def test_patch_book_rating_success(self):
        """Test successful changing of a book rating"""

        response = self.client().post('/books', json=self.new_book)
        created_book_id = response.json.get('created_book_id')
        response = self.client().patch(
            f'/books/{created_book_id}',
            json={'rating': 1},
        )
        book = Book.query.get(created_book_id)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json.get('success'))
        self.assertEqual(response.json.get('updated_book_id'), created_book_id)
        self.assertEqual(book.rating, 1)

    def test_patch_book_rating_out_of_range_fail(self):
        """Test failed book rating change when book does not exist"""

        response = self.client().post('/books', json=self.new_book)
        created_book_id = response.json.get('created_book_id')
        response = self.client().patch(
            f'/books/{created_book_id+1}',
            json={'rating': 1},
        )

        self.assertEqual(response.status_code, 422)
        self.assertFalse(response.json.get('success'))
        self.assertEqual(response.json.get('message'), 'Unprocessable Entity')

    def test_patch_book_rating_no_rating_fail(self):
        """Test failed book rating change when no rating is given"""

        response = self.client().post('/books', json=self.new_book)
        created_book_id = response.json.get('created_book_id')
        response = self.client().patch(f'/books/{created_book_id}',)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json.get('success'))
        self.assertEqual(response.json.get('message'), 'Bad Request')

    def test_delete_book_success(self):
        """Test successful deletion of a book"""

        response = self.client().post('/books', json=self.new_book)
        created_book_id = response.json.get('created_book_id')
        response = self.client().delete(f'/books/{created_book_id}')
        book = Book.query.get(created_book_id)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json.get('success'))
        self.assertEqual(response.json.get('deleted_book_id'), created_book_id)
        self.assertTrue(response.json.get('books'))
        self.assertTrue(response.json.get('total_books'))
        self.assertIsNone(book)

    def test_delete_out_of_range_fail(self):
        """Test failed book deletion when book does not exist"""

        response = self.client().post('/books', json=self.new_book)
        created_book_id = response.json.get('created_book_id')
        response = self.client().delete(f'/books/{created_book_id+1}')

        self.assertEqual(response.status_code, 422)
        self.assertFalse(response.json.get('success'))
        self.assertEqual(response.json.get('message'), 'Unprocessable Entity')

    def test_books_patch_method_not_allowed_fail(self):
        """Test that patch method is not allowed at /books endpoint"""

        response = self.client().patch('/books')

        self.assertEqual(response.status_code, 405)
        self.assertFalse(response.json.get('success'))
        self.assertEqual(response.json.get('message'), 'Method Not Allowed')

    def test_books_delete_method_not_allowed_fail(self):
        """Test that delete method is not allowed at /books endpoint"""

        response = self.client().delete('/books')

        self.assertEqual(response.status_code, 405)
        self.assertFalse(response.json.get('success'))
        self.assertEqual(response.json.get('message'), 'Method Not Allowed')

    def test_book_get_method_not_allowed_fail(self):
        """Test that get method is not allowed at /books/id endpoint"""

        response = self.client().post('/books', json=self.new_book)
        created_book_id = response.json.get('created_book_id')
        response = self.client().get(f'/books/{created_book_id}')

        self.assertEqual(response.status_code, 405)
        self.assertFalse(response.json.get('success'))
        self.assertEqual(response.json.get('message'), 'Method Not Allowed')

    def test_book_post_method_not_allowed_fail(self):
        """Test that post method is not allowed at /books/id endpoint"""

        response = self.client().post('/books', json=self.new_book)
        created_book_id = response.json.get('created_book_id')
        response = self.client().post(f'books/{created_book_id}')

        self.assertEqual(response.status_code, 405)
        self.assertFalse(response.json.get('success'))
        self.assertEqual(response.json.get('message'), 'Method Not Allowed')


if __name__ == "__main__":
    unittest.main()
