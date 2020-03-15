"""A virtual bookshelf.

User are able to add their books to the bookshelf, give them a rating, update
the rating and search through their book lists.

    Usage: flask run
"""

import os
import random
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Book

BOOKS_PER_SHELF = 8


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

    def paginate_books(request, books):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * BOOKS_PER_SHELF
        end = start + BOOKS_PER_SHELF
        books = [book.format() for book in books]
        return books[start:end]

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
            'Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS'
        )
        return response

    @app.route('/books')
    def get_books():
        """Route handler for endpoint showing all books

        Returns:
            response: A json object representing all books
        """

        books = Book.query.order_by(Book.id).all()
        current_books = paginate_books(request, books)
        if not current_books:
            abort(404)

        response = jsonify({
            'success': True,
            'books': current_books,
            'total_books': len(books),
        })

        return response

    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def patch_book_rating(book_id):
        """Route handler for endpoint updating the rating of a single book

        Args:
            book_id: An int representing the identifier for the book to update
                the rating of

        Returns:
            response: A json object stating if the request was successful
        """

        book = Book.query.get(book_id)
        if book is None:
            abort(404)

        rating = request.json.get('rating')
        if rating:
            book.rating = int(rating)

        try:
            book.update()
        except Exception:  # pylint: disable=broad-except
            abort(500)

        response = jsonify({
            'success': True,
            'updated_book_id': book_id,
        })

        return response

    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        """Route handler for endpoint to delete a single book

        Args:
            book_id: An int representing the identifier for a book to delete

        Returns:
            response: A json object containing the id of the book that was
                deleted and a list of the remaining books
        """

        book = Book.query.get(book_id)
        if book is None:
            abort(404)

        try:
            book.delete()
        except Exception:  # pylint: disable=broad-except
            abort(500)

        books = Book.query.order_by(Book.id).all()
        current_books = paginate_books(request, books)
        if not current_books:
            abort(404)

        response = jsonify({
            'success': True,
            'deleted_book_id': book_id,
            'books': current_books,
            'total_books': len(books),
        })

        return response

    @app.route('/books', methods=['POST'])
    def create_book():
        """Route handler for endpoint to create a book

        Returns:
            response: A json object containing the id of the book that was
                created and a list of the remaining books
        """
        book = Book(
            title=request.json.get('title'),
            author=request.json.get('author'),
            rating=request.json.get('rating'),
        )
        book.insert()
        books = Book.query.all()
        books = [book.format() for book in books]

        response = jsonify({
            'success': True,
            'create_book_id': book.id,
            'books': books,
            'total_books': len(books),
        })

        return response

    return app
