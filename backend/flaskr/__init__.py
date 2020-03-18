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


def paginate_books(books, page):
    """Retrieve books for the current page only

    Args:
        request: A flask request object
        books: A list of book objects

    Returns:
        A list of book objects for the given page formatted into a dict
    """

    books = [book.format() for book in books]
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF

    current_books = books[start:end]
    if not current_books:
        abort(404)

    return current_books


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
    page = request.args.get('page', 1, type=int)
    current_books = paginate_books(books, page)

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
        abort(422)

    try:

        rating = request.json.get('rating')
        if rating:
            book.rating = int(rating)

        book.update()

    except AttributeError:
        abort(400)

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
        abort(422)

    try:
        book.delete()
    except Exception:  # pylint: disable=broad-except
        abort(500)

    books = Book.query.order_by(Book.id).all()
    page = request.args.get('page', 1, type=int)
    current_books = paginate_books(books, page)

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
    except AttributeError:
        abort(400)

    books = Book.query.order_by(Book.id).all()
    page = request.args.get('page', 1, type=int)
    current_books = paginate_books(books, page)

    response = jsonify({
        'success': True,
        'create_book_id': book_id,
        'books': current_books,
        'total_books': len(books),
    })

    return response


@app.errorhandler(400)
def bad_request(error):  # pylint: disable=unused-argument
    """Error handler for 400 bad request

    Args:
        error: unused

    Returns:
        Response: A json object with the error code and message
    """
    response = jsonify({
        'success': False,
        'error_code': 400,
        'message': 'Bad Request',
    })
    return response, 400


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


@app.errorhandler(422)
def unprocessable_entity(error):  # pylint: disable=unused-argument
    """Error handler for 422 unprocessable entity

    Args:
        error: unused

    Returns:
        Response: A json object with the error code and message
    """
    response = jsonify({
        'success': False,
        'error_code': 422,
        'message': 'Unprocessable Entity',
    })
    return response, 422
