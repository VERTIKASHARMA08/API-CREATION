from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask import render_template  # Add this at the top

load_dotenv()

print("DB URL:", os.getenv("DATABASE_URL"))  # Debug line

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{"id": b.id, "title": b.title, "author": b.author, "price": b.price} for b in books])

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(
        id=data.get('id'),  # use custom ID if provided
        title=data['title'],
        author=data['author'],
        price=data['price']
    )
    db.session.add(new_book)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    return jsonify({"message": "Book added"}), 201

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Validate required fields
    for field in ['title', 'author', 'price']:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Optional: Update ID if provided and different
    new_id = data.get('id')
    if new_id and new_id != id:
        existing = Book.query.get(new_id)
        if existing:
            return jsonify({"error": "A book with this new ID already exists."}), 409
        book.id = new_id  # Manual primary key change

    # Update other fields
    book.title = data['title']
    book.author = data['author']
    book.price = data['price']

    db.session.commit()
    return jsonify({
        "message": "Book updated successfully",
        "book": {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "price": book.price
        }
    }), 200


@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"})

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "price": book.price
    })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
