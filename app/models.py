from datetime import datetime

from . import db

association_table = db.Table('author2book', db.Model.metadata,
    db.Column('author_id', db.ForeignKey('authors.id'), primary_key=True),
    db.Column('book_id', db.ForeignKey('books.id'), primary_key=True)
)

association_table2 = db.Table('publisher2book', db.Model.metadata,
    db.Column('publisher_id', db.ForeignKey('publishers.id'), primary_key=True),
    db.Column('book_id', db.ForeignKey('books.id'), primary_key=True)
)

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    year = db.Column(db.Integer)

    authors = db.relationship('Author', secondary=association_table, back_populates='books')
    publishers = db.relationship('Publisher', secondary=association_table2, back_populates='books')

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(512))

    books = db.relationship('Book', secondary=association_table, back_populates='authors')


class Publisher(db.Model):
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))

    books = db.relationship('Book', secondary=association_table2, back_populates='publishers')