from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models.book import Book, Category, Author
from app.models.loan import Loan, Reservation
from app.forms.book import SearchForm
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    # Get featured books (most borrowed)
    featured_books = Book.query.join(Loan).group_by(Book.id).order_by(
        func.count(Loan.id).desc()
    ).limit(5).all()
    
    # Get recent additions
    recent_books = Book.query.order_by(Book.created_at.desc()).limit(5).all()
    
    # Get popular categories
    popular_categories = Category.query.join(Book).join(Loan).group_by(Category.id).order_by(
        func.count(Loan.id).desc()
    ).limit(5).all()
    
    return render_template('main/index.html',
                         title='Home',
                         featured_books=featured_books,
                         recent_books=recent_books,
                         popular_categories=popular_categories)

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get user's current loans
    current_loans = Loan.query.filter_by(
        user_id=current_user.id,
        returned=False
    ).all()
    
    # Get user's overdue books
    overdue_books = Loan.query.filter(
        Loan.user_id == current_user.id,
        Loan.returned == False,
        Loan.due_date < datetime.utcnow()
    ).all()
    
    # Get user's active reservations
    active_reservations = Reservation.query.filter(
        Reservation.user_id == current_user.id,
        Reservation.status == 'pending',
        Reservation.expires_at > datetime.utcnow()
    ).all()
    
    # Get user's borrowing history
    borrowing_history = Loan.query.filter_by(
        user_id=current_user.id
    ).order_by(Loan.borrowed_at.desc()).limit(5).all()
    
    return render_template('main/dashboard.html',
                         title='Dashboard',
                         current_loans=current_loans,
                         overdue_books=overdue_books,
                         active_reservations=active_reservations,
                         borrowing_history=borrowing_history)

@bp.route('/search')
def search():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.query.data
        search_by = form.search_by.data
        
        if search_by == 'title':
            books = Book.query.filter(Book.title.ilike(f'%{query}%')).all()
        elif search_by == 'author':
            books = Book.query.join(Author).filter(Author.name.ilike(f'%{query}%')).all()
        elif search_by == 'isbn':
            books = Book.query.filter(Book.isbn.ilike(f'%{query}%')).all()
        else:  # category
            books = Book.query.join(Category).filter(Category.name.ilike(f'%{query}%')).all()
        
        return render_template('main/search_results.html',
                             title='Search Results',
                             books=books,
                             query=query)
    
    return render_template('main/search.html',
                         title='Search',
                         form=form)

@bp.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html',
                         title='Profile',
                         user=current_user) 