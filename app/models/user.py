from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='user')  # user, librarian, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    loans = db.relationship('Loan', backref='user', lazy='dynamic')
    reservations = db.relationship('Reservation', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def can_borrow(self):
        """Check if user can borrow more books"""
        active_loans = self.loans.filter_by(returned=False).count()
        return active_loans < current_app.config['MAX_BOOKS_PER_USER']
    
    def get_borrowing_history(self):
        """Get user's borrowing history"""
        return self.loans.order_by(Loan.borrowed_at.desc()).all()
    
    def get_overdue_books(self):
        """Get list of overdue books"""
        return self.loans.filter_by(returned=False).filter(
            Loan.due_date < datetime.utcnow()
        ).all()
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 