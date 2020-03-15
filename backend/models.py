import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "bookshelf"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
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
