from datetime import datetime

from . import db

association_table = db.Table('author2book', db.Model.metadata,
    db.Column('author_id', db.Integer, db.ForeignKey('authors.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'))
)

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    year = db.Column(db.Integer)

    publishers = db.relationship('Publisher', backref='publisher', lazy='dynamic')
    authors = db.relationship('Author', secondary=association_table)

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(512))

    books = db.relationship('Book', secondary=association_table)


class Publisher(db.Model):
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))