from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'  # SQLite database
db = SQLAlchemy(app)

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(20), nullable=False)

    def __init__(self, title, author, year_published, genre):
        self.title = title
        self.author = author
        self.year_published = year_published
        self.genre = genre

# Create the database tables
with app.app_context():
    db.create_all()

# index.html
@app.route('/')
def index():
    return render_template('index.html')

# Create a new book
# Create a new book
@app.route('/books', methods=["POST"])
def create_book():
    data = request.json
    title = data.get('title')
    author = data.get('author')
    year_published = data.get('year_published')
    genre = data.get('genre')

    if not title or not author or not year_published or not genre:
        return 'Incomplete book data', 400

    # Create a new book object with the provided parameters
    new_book = Book(title=title, author=author, year_published=year_published, genre=genre)
    
    # Add the new book to the database session
    db.session.add(new_book)
    
    # Commit the changes to the database
    db.session.commit()
    
    return 'Book added successfully'


# Get all books
@app.route('/books', methods=["GET"])
def get_all_books():
    books = Book.query.all()
    if not books:
        return 'No books in inventory'
    book_list = [{'id': book.id, 'title': book.title, 'author': book.author, 'year_published': book.year_published, 'genre': book.genre} for book in books]
    return jsonify(book_list)

# Get book by ID
@app.route('/books/<int:id>', methods=["GET"])
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return 'Book not found', 404
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'year_published': book.year_published, 'genre': book.genre})

# Update book by ID
@app.route('/books/<int:id>', methods=["PUT"])
def update_book(id):
    data = request.json
    book = Book.query.get(id)
    if not book:
        return 'Book not found', 404

    title = data.get('title', book.title)
    author = data.get('author', book.author)
    year_published = data.get('year_published', book.year_published)
    genre = data.get('genre', book.genre)

    book.title = title
    book.author = author
    book.year_published = year_published
    book.genre = genre

    db.session.commit()
    return 'Book updated successfully'

# Delete book by ID
@app.route('/books/<int:id>', methods=["DELETE"])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return 'Book not found', 404
    db.session.delete(book)
    db.session.commit()
    return 'Book deleted successfully'

if __name__ == '__main__':
    app.run(debug=True)
