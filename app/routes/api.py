from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.book import Book, Category, Author
from app.models.loan import Loan, Reservation
from datetime import datetime, timedelta
from functools import wraps

bp = Blueprint('api', __name__)

def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != current_app.config['API_KEY']:
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/books')
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    books = Book.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'books': [{
            'id': book.id,
            'title': book.title,
            'isbn': book.isbn,
            'author': book.author.name,
            'category': book.category.name,
            'available': book.available,
            'total': book.quantity
        } for book in books.items],
        'total': books.total,
        'pages': books.pages,
        'current_page': books.page
    })

@bp.route('/books/<int:id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'isbn': book.isbn,
        'publisher': book.publisher,
        'publication_year': book.publication_year,
        'edition': book.edition,
        'description': book.description,
        'author': {
            'id': book.author.id,
            'name': book.author.name
        },
        'category': {
            'id': book.category.id,
            'name': book.category.name
        },
        'available': book.available,
        'total': book.quantity,
        'location': book.location
    })

@bp.route('/books/search')
def search_books():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Search query is required'}), 400
    
    books = Book.query.filter(
        (Book.title.ilike(f'%{query}%')) |
        (Book.isbn.ilike(f'%{query}%')) |
        (Author.name.ilike(f'%{query}%'))
    ).join(Author).all()
    
    return jsonify({
        'books': [{
            'id': book.id,
            'title': book.title,
            'isbn': book.isbn,
            'author': book.author.name,
            'available': book.available
        } for book in books]
    })

@bp.route('/loans', methods=['GET'])
@api_key_required
def get_loans():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    loans = Loan.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'loans': [{
            'id': loan.id,
            'book': {
                'id': loan.book.id,
                'title': loan.book.title
            },
            'user': {
                'id': loan.user.id,
                'username': loan.user.username
            },
            'borrowed_at': loan.borrowed_at.isoformat(),
            'due_date': loan.due_date.isoformat(),
            'returned': loan.returned
        } for loan in loans.items],
        'total': loans.total,
        'pages': loans.pages,
        'current_page': loans.page
    })

@bp.route('/loans', methods=['POST'])
@api_key_required
def create_loan():
    data = request.get_json()
    if not data or 'book_id' not in data or 'user_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    book = Book.query.get_or_404(data['book_id'])
    if not book.is_available():
        return jsonify({'error': 'Book is not available'}), 400
    
    loan = Loan(
        book_id=data['book_id'],
        user_id=data['user_id'],
        due_date=datetime.utcnow() + timedelta(days=current_app.config['LOAN_PERIOD_DAYS'])
    )
    
    book.available -= 1
    db.session.add(loan)
    db.session.commit()
    
    return jsonify({
        'id': loan.id,
        'book': {
            'id': loan.book.id,
            'title': loan.book.title
        },
        'user': {
            'id': loan.user.id,
            'username': loan.user.username
        },
        'borrowed_at': loan.borrowed_at.isoformat(),
        'due_date': loan.due_date.isoformat()
    }), 201

@bp.route('/loans/<int:id>/return', methods=['POST'])
@api_key_required
def return_book(id):
    loan = Loan.query.get_or_404(id)
    if loan.returned:
        return jsonify({'error': 'Book already returned'}), 400
    
    loan.return_book()
    db.session.commit()
    
    return jsonify({
        'id': loan.id,
        'returned_at': loan.returned_at.isoformat(),
        'fine_amount': loan.fine_amount
    }) 