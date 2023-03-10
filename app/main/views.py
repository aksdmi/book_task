from flask import request, current_app, render_template
from . import main
from .. import db
from ..models import Book
from . forms import BookForm



@main.route('/', methods=['GET', 'POST'])
def index():
    form = BookForm()
    page = request.args.get('page', 1, type=int)
    query = Book.query
    pagination = query.order_by(Book.year.desc()).paginate(
        page=page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination)

