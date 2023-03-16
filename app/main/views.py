from flask import request, current_app, render_template, redirect, url_for, flash
from . import main
from .. import db
from ..models import Book, Author, Publisher
from . forms import BookForm, AuthorForm, PublisherForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, year=form.year.data)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    query = Book.query
    pagination = query.order_by(Book.year.desc()).paginate(
        page=page, per_page=current_app.config['FLASKY_BOOKS_PER_PAGE'],
        error_out=False)
    books = pagination.items
    return render_template('index.html', form=form, books=books, pagination=pagination)


def insert_update_book(form: BookForm, book: Book, msg: str, endpoint: str):
    book.title = form.title.data
    book.year = form.year.data
    book.authors = []
    for itm in form.authors.data:
        book.authors.append(Author.query.get_or_404(itm))

    book.publishers = []
    for itm in form.publishers.data:
        book.publishers.append(Publisher.query.get_or_404(itm))

    db.session.add(book)
    db.session.commit()
    flash(msg)
    return redirect(url_for(endpoint))


def update_defaults(form: BookForm, book: Book):
    # authors
    form.authors.default = []
    for row in book.authors:
        form.authors.default.append(row.id)

    # publishers
    form.publishers.default = []
    for row in book.publishers:
        form.publishers.default.append(row.id)

    form.process()

    return form


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    book = Book.query.get_or_404(id)
    form = BookForm()

    # authors
    form.authors.choices = []
    for row in Author.query.order_by(Author.fio.asc()):
        form.authors.choices.append((row.id, row.fio))

    # publishers
    form.publishers.choices = []
    for row in Publisher.query.order_by(Publisher.name.asc()):
        form.publishers.choices.append((row.id, row.name))

    if form.validate_on_submit():
        msg = f'Данные о книге "{book.title}" были обновлены.'
        return insert_update_book(form, book, msg, '.index')

    form = update_defaults(form, book)

    form.title.data = book.title
    form.year.data = book.year

    return render_template('edit_book.html', form=form)

@main.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    book = Book.query.get_or_404(id)
    msg = f'Данные книги {book.title} удалены'
    db.session.delete(book)
    db.session.commit()
    flash(msg)
    return redirect(url_for('.index'))


@main.route('/new', methods=['GET', 'POST'])
def new():
    form = BookForm()
    book = Book()

    # authors
    form.authors.choices = []
    for row in Author.query.order_by(Author.fio.asc()):
        form.authors.choices.append((row.id, row.fio))

    # publishers
    form.publishers.choices = []
    for row in Publisher.query.order_by(Publisher.name.asc()):
        form.publishers.choices.append((row.id, row.name))

    if form.validate_on_submit():
        msg = f'Данные о книге {book.title} были добавлены.'
        return insert_update_book(form, book, msg, '.index')

    form = update_defaults(form, book)

    return render_template('edit_book.html', form=form)


@main.route('/authors', methods=['GET'])
def authors():
    authors = Author.query.order_by(Author.fio.asc())
    return render_template('authors.html', authors=authors)


@main.route('/authors/new', methods=['GET', 'POST'])
def authors_new():
    form = AuthorForm()
    if form.validate_on_submit():
        msg = f'Добавлен новый автор "{form.fio.data}"'

        author = Author()
        author.fio = form.fio.data

        db.session.add(author)
        db.session.commit()
        flash(msg)
        return redirect(url_for('.authors'))

    return render_template('edit_author.html', form=form)

@main.route('/authors/edit/<int:id>', methods=['GET', 'POST'])
def authors_edit(id):
    author = Author.query.get_or_404(id)
    form = AuthorForm()

    if form.validate_on_submit():

        msg = f'Обновлен автор "{author.fio}" -> "{form.fio.data}"'
        author.fio = form.fio.data
        db.session.add(author)
        db.session.commit()
        flash(msg)
        return redirect(url_for('.authors'))

    form.fio.data = author.fio

    return render_template('edit_author.html', form=form)

@main.route('/authors/delete/<int:id>', methods=['GET'])
def authors_delete(id):
    author = Author.query.get_or_404(id)

    msg = f'Удален автор "{author.fio}"'
    db.session.delete(author)
    db.session.commit()
    flash(msg)
    return redirect(url_for('.authors'))

@main.route('/publishers', methods=['GET'])
def publishers():
    publishers = Publisher.query.order_by(Publisher.name.asc())
    return render_template('publishers.html', publishers=publishers)


@main.route('/publishers/new', methods=['GET', 'POST'])
def publishers_new():
    form = PublisherForm()
    if form.validate_on_submit():
        msg = f'Добавлен новый издатель "{form.name.data}"'

        publisher = Publisher()
        publisher.name = form.name.data

        db.session.add(publisher)
        db.session.commit()
        flash(msg)
        return redirect(url_for('.publishers'))

    return render_template('edit_publisher.html', form=form)

@main.route('/publishers/edit/<int:id>', methods=['GET', 'POST'])
def publishers_edit(id):
    publisher = Publisher.query.get_or_404(id)
    form = PublisherForm()

    if form.validate_on_submit():
        msg = f'Обновлен издатель "{publisher.name}" -> "{form.name.data}"'

        publisher.name = form.name.data



        db.session.add(publisher)
        db.session.commit()
        flash(msg)
        return redirect(url_for('.publishers'))

    form.name.data = publisher.name

    return render_template('edit_publisher.html', form=form)

@main.route('/publishers/delete/<int:id>', methods=['GET'])
def publishers_delete(id):
    publisher = Publisher.query.get_or_404(id)

    msg = f'Удален издатель "{publisher.name}"'
    db.session.delete(publisher)
    db.session.commit()
    flash(msg)
    return redirect(url_for('.publishers'))