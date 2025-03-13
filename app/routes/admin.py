from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.book import Book, Category, Author
from app.models.loan import Loan, Reservation
from datetime import datetime
from sqlalchemy import func
from functools import wraps

bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/admin')
@admin_required
def admin_dashboard():
    # Get system statistics
    total_users = User.query.count()
    total_books = Book.query.count()
    total_loans = Loan.query.count()
    total_reservations = Reservation.query.count()
    
    # Get recent activities
    recent_loans = Loan.query.order_by(Loan.borrowed_at.desc()).limit(5).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    # Get overdue books
    overdue_books = Loan.query.filter(
        Loan.returned == False,
        Loan.due_date < datetime.utcnow()
    ).all()
    
    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         total_users=total_users,
                         total_books=total_books,
                         total_loans=total_loans,
                         total_reservations=total_reservations,
                         recent_loans=recent_loans,
                         recent_users=recent_users,
                         overdue_books=overdue_books)

@bp.route('/admin/users')
@admin_required
def user_list():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.username).paginate(
        page=page,
        per_page=20,
        error_out=False
    )
    return render_template('admin/users.html',
                         title='User Management',
                         users=users)

@bp.route('/admin/users/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.role = request.form.get('role')
        user.is_active = 'is_active' in request.form
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin.user_list'))
    return render_template('admin/edit_user.html',
                         title='Edit User',
                         user=user)

@bp.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def system_settings():
    if request.method == 'POST':
        # TODO: Implement system settings update
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('admin.system_settings'))
    return render_template('admin/settings.html',
                         title='System Settings')

@bp.route('/admin/reports')
@admin_required
def reports():
    # Get loan statistics
    total_loans = Loan.query.count()
    active_loans = Loan.query.filter_by(returned=False).count()
    overdue_loans = Loan.query.filter(
        Loan.returned == False,
        Loan.due_date < datetime.utcnow()
    ).count()
    
    # Get popular books
    popular_books = Book.query.join(Loan).group_by(Book.id).order_by(
        func.count(Loan.id).desc()
    ).limit(10).all()
    
    # Get popular categories
    popular_categories = Category.query.join(Book).join(Loan).group_by(Category.id).order_by(
        func.count(Loan.id).desc()
    ).limit(5).all()
    
    return render_template('admin/reports.html',
                         title='Reports',
                         total_loans=total_loans,
                         active_loans=active_loans,
                         overdue_loans=overdue_loans,
                         popular_books=popular_books,
                         popular_categories=popular_categories) 