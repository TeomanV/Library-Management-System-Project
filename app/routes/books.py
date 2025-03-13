from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.book import Book, Category, Author
from app.models.loan import Loan, Reservation
from app.forms.book import BookForm, CategoryForm, AuthorForm
from datetime import datetime, timedelta

bp = Blueprint('books', __name__)

@bp.route('/books')
def book_list():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    author_id = request.args.get('author', type=int)
    
    query = Book.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    if author_id:
        query = query.filter_by(author_id=author_id)
    
    books = query.order_by(Book.title).paginate(
        page=page,
        per_page=current_app.config['BOOKS_PER_PAGE'],
        error_out=False
    )
    
    categories = Category.query.order_by(Category.name).all()
    authors = Author.query.order_by(Author.name).all()
    
    return render_template('books/list.html',
                         title='Books',
                         books=books,
                         categories=categories,
                         authors=authors)

@bp.route('/books/<int:id>')
def book_detail(id):
    book = Book.query.get_or_404(id)
    return render_template('books/detail.html',
                         title=book.title,
                         book=book)

@bp.route('/books/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if current_user.role not in ['librarian', 'admin']:
        flash('You do not have permission to add books.', 'danger')
        return redirect(url_for('main.index'))
    
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            isbn=form.isbn.data,
            publisher=form.publisher.data,
            publication_year=form.publication_year.data,
            edition=form.edition.data,
            description=form.description.data,
            quantity=form.quantity.data,
            available=form.quantity.data,
            location=form.location.data,
            category_id=form.category_id.data,
            author_id=form.author_id.data
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('books.book_detail', id=book.id))
    
    return render_template('books/form.html',
                         title='Add Book',
                         form=form)

@bp.route('/books/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    if current_user.role not in ['librarian', 'admin']:
        flash('You do not have permission to edit books.', 'danger')
        return redirect(url_for('main.index'))
    
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.isbn = form.isbn.data
        book.publisher = form.publisher.data
        book.publication_year = form.publication_year.data
        book.edition = form.edition.data
        book.description = form.description.data
        book.quantity = form.quantity.data
        book.location = form.location.data
        book.category_id = form.category_id.data
        book.author_id = form.author_id.data
        
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('books.book_detail', id=book.id))
    
    return render_template('books/form.html',
                         title='Edit Book',
                         form=form,
                         book=book)

@bp.route('/books/<int:id>/borrow', methods=['POST'])
@login_required
def borrow_book(id):
    book = Book.query.get_or_404(id)
    
    if not book.is_available():
        flash('This book is not available for borrowing.', 'warning')
        return redirect(url_for('books.book_detail', id=book.id))
    
    if not current_user.can_borrow():
        flash('You have reached the maximum number of books you can borrow.', 'warning')
        return redirect(url_for('books.book_detail', id=book.id))
    
    loan = Loan(
        user_id=current_user.id,
        book_id=book.id,
        due_date=datetime.utcnow() + timedelta(days=current_app.config['LOAN_PERIOD_DAYS'])
    )
    
    book.available -= 1
    db.session.add(loan)
    db.session.commit()
    
    flash('Book borrowed successfully!', 'success')
    return redirect(url_for('books.book_detail', id=book.id))

@bp.route('/books/<int:id>/reserve', methods=['POST'])
@login_required
def reserve_book(id):
    book = Book.query.get_or_404(id)
    
    if not book.can_be_reserved():
        flash('This book cannot be reserved at the moment.', 'warning')
        return redirect(url_for('books.book_detail', id=book.id))
    
    reservation = Reservation(
        user_id=current_user.id,
        book_id=book.id,
        expires_at=datetime.utcnow() + timedelta(days=3)
    )
    
    db.session.add(reservation)
    db.session.commit()
    
    flash('Book reserved successfully!', 'success')
    return redirect(url_for('books.book_detail', id=book.id)) 