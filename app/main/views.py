from flask import request, current_app, render_template, redirect, url_for, flash
from . import main
from .. import db
from ..models import Book
from . forms import BookForm



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

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    book = Book.query.get_or_404(id)

    form = BookForm()
    if form.validate_on_submit():
        book.title = form.title.data
        book.year = form.year.data
        db.session.add(book)
        db.session.commit()
        flash('The book has been updated.')
        return redirect(url_for('.index'))
    form.title.data = book.title
    form.year.data = book.year
    return render_template('edit_book.html', form=form)