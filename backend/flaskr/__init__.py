import os
import random
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Book

BOOKS_PER_SHELF = 8

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO'
#     within the frontend to update the endpoints there. If you do not update
#     the endpoints, the lab will not work - of no fault of your API code!
#   - Make sure for each route that you're thinking through when to abort and
#     with which kind of error
#   - If you change any of the response body keys, make sure you update the
#     frontend to correspond.


def create_app(test_config=None):
    """Creates flask app and defines its routes

    Args:
        test_config: Config object for testing, defaults to none

    Returns:
        app: A flask application
    """

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        """Adds response headers after request

        Args:
            response: The response object to add headers to

        Returns:
            response: The response object that the headers were added to
        """
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type, Authorization, true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS'
        )
        return response

    @app.route('/books')
    def get_books():
        """Route handler for endpoint showing all books

        Returns:
            response: A json object representing all books
        """
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * BOOKS_PER_SHELF
        end = start + BOOKS_PER_SHELF
        books = Book.query.all()
        books = [book.format() for book in books]
        response = jsonify({
            'success': True,
            'books': books[start:end],
            'total_books': len(books),
        })

        return response

    # @TODO: Write a route that will update a single book's rating.
    #        It should only be able to update the rating, not the entire
    #           representation
    #        and should follow API design principles regarding method and
    #           route.
    #        Response body keys: 'success'
    # TEST: When completed, you will be able to click on stars to update a
    #       book's rating and it will persist after refresh

    # @TODO: Write a route that will delete a single book.
    #        Response body keys: 'success', 'deleted'(id of deleted book),
    #           'books' and 'total_books'
    #        Response body keys: 'success', 'books' and 'total_books'

    # TEST: When completed, you will be able to delete a single book by
    #       clicking on the trashcan.

    # @TODO: Write a route that create a new book.
    #        Response body keys: 'success', 'created'(id of created book),
    #           'books' and 'total_books'
    # TEST: When completed, you will be able to a new book using the form. Try
    #           doing so from the last page of books.
    #       Your new book should show up immediately after you submit it at
    #           the end of the page.

    return app
