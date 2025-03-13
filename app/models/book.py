from datetime import datetime
from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    publisher = db.Column(db.String(100))
    publication_year = db.Column(db.Integer)
    edition = db.Column(db.String(50))
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(200))
    quantity = db.Column(db.Integer, default=1)
    available = db.Column(db.Integer, default=1)
    location = db.Column(db.String(50))  # Shelf/rack location
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    
    # Relationships
    category = db.relationship('Category', backref='books')
    author = db.relationship('Author', backref='books')
    loans = db.relationship('Loan', backref='book', lazy='dynamic')
    reservations = db.relationship('Reservation', backref='book', lazy='dynamic')
    
    def is_available(self):
        """Check if book is available for borrowing"""
        return self.available > 0
    
    def can_be_reserved(self):
        """Check if book can be reserved"""
        return self.available > 0 or self.reservations.count() < self.quantity
    
    def get_loan_history(self):
        """Get book's loan history"""
        return self.loans.order_by(Loan.borrowed_at.desc()).all()
    
    def get_current_loan(self):
        """Get current active loan if any"""
        return self.loans.filter_by(returned=False).first()
    
    def __repr__(self):
        return f'<Book {self.title}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    biography = db.Column(db.Text)
    birth_date = db.Column(db.Date)
    death_date = db.Column(db.Date)
    
    def __repr__(self):
        return f'<Author {self.name}>' 