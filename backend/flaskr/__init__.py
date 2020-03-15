"""A virtual bookshelf.

User are able to add their books to the bookshelf, give them a rating, update
the rating and search through their book lists.

Attributes:
    app: A flask Flack object creating the flask app

    Usage: flask run
"""

import os
import random
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Book

BOOKS_PER_SHELF = 8

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

    try:
        book = Book(
            title=request.json.get('title'),
            author=request.json.get('author'),
            rating=request.json.get('rating'),
        )
        book.insert()
        book_id = book.id
    except Exception:  # pylint: disable=broad-except
        abort(500)

    books = Book.query.order_by(Book.id).all()
    current_books = paginate_books(request, books)
    if not current_books:
        abort(404)

    response = jsonify({
        'success': True,
        'create_book_id': book_id,
        'books': current_books,
        'total_books': len(books),
    })

    return response


@app.errorhandler(404)
def not_found(error):  # pylint: disable=unused-argument
    """Error handler for 404 not found

    Args:
        error: unused

    Returns:
        Response: A json object with the error code and message
    """
    response = jsonify({
        'success': False,
        'error_code': 404,
        'message': 'Not Found',
    })
    return response, 404


@app.errorhandler(405)
def method_not_allowed(error):  # pylint: disable=unused-argument
    """Error handler for 405 method not allowed

    Args:
        error: unused

    Returns:
        Response: A json object with the error code and message
    """
    response = jsonify({
        'success': False,
        'error_code': 405,
        'message': 'Method Not Allowed',
    })
    return response, 405


@app.errorhandler(500)
def internal_server_error(error):  # pylint: disable=unused-argument
    """Error handler for 500 internal server error

    Args:
        error: unused

    Returns:
        Response: A json object with the error code and message
    """
    response = jsonify({
        'success': False,
        'error_code': 500,
        'message': 'Internal Server Error',
    })
    return response, 500
