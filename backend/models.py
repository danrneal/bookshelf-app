"""Model objects used to model data for the db

Attributes:
    DB_DIALECT: A str representing the dialect of the db
    DB_USER: A str representing the username to use with the db
    DB_PASS: A str representing the DB_USER's password
    DB_HOST: A str representing the host of the db
    DB_PORT: An int representing the port the db is running on
    DB_NAME: A str representing the db in which to connect to
    DB_PATH: A str representing the location of the db
    db: A SQLAlchemy service
"""

from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

DB_DIALECT = 'postgresql'
DB_USER = 'dneal'
DB_PASS = ''
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'bookshelf'

DB_PATH = f'{DB_DIALECT}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

db = SQLAlchemy()


def setup_db(app, database_path=DB_PATH):
    """Binds a flask application and SQLAlchemy service

    Args:
        app: A flask app
        database_path: A str representing the location of the db
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Book(db.Model):
    """A model representing a Book

    Attributes:
        id: An int that serves as the unique identifier for a book
        title: A str representing the title of a book
        author: A str representing the author of a book
        rating: An int representing the rating of a book
    """

    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    rating = Column(Integer)

    def __init__(self, title, author, rating):
        self.title = title
        self.author = author
        self.rating = rating

    def insert(self):
        """Inserts a new book object into the db"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates an existing book object in the db"""
        db.session.commit()

    def delete(self):
        """Deletes an existing book object from the db"""
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """Formats the book object as a dict

        Returns:
            plant: A dict representing the book object
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'rating': self.rating,
        }
