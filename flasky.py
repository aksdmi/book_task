import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import Book, Author, Publisher


app = create_app('production')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, book=Book, author=Author, publisher=Publisher)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)