from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
database.init_app(app)


class Books(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(250), nullable=False, unique=True)
    author = database.Column(database.String(250), nullable=False)
    rating = database.Column(database.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    database.create_all()


@app.route('/')
def home():
    result = database.session.execute(database.select(Books).order_by(Books.title))
    all_books = result.scalars()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        new_book = Books(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        database.session.add(new_book)
        database.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit", methods=['POST', 'GET'])
def edit():
    if request.method == 'POST':
        book_id = request.form['id']
        book_to_update = database.get_or_404(Books, book_id)
        book_to_update.rating = request.form['rating']
        database.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = database.get_or_404(Books, book_id)
    return render_template('edit.html', book=book_selected)

@app.route('/delete')
def delete():
    book_id = request.args.get('id')
    book_to_delete = database.get_or_404(Books, book_id)
    database.session.delete(book_to_delete)
    database.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
