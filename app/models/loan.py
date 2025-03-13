from datetime import datetime, timedelta
from app import db, current_app

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrowed_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    returned_at = db.Column(db.DateTime)
    returned = db.Column(db.Boolean, default=False)
    fine_amount = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)
    
    def calculate_fine(self):
        """Calculate fine for overdue books"""
        if not self.returned and self.due_date < datetime.utcnow():
            days_overdue = (datetime.utcnow() - self.due_date).days
            return days_overdue * current_app.config['FINE_PER_DAY']
        return 0.0
    
    def is_overdue(self):
        """Check if loan is overdue"""
        return not self.returned and self.due_date < datetime.utcnow()
    
    def return_book(self):
        """Process book return"""
        if not self.returned:
            self.returned = True
            self.returned_at = datetime.utcnow()
            self.fine_amount = self.calculate_fine()
            self.book.available += 1
            return True
        return False
    
    def __repr__(self):
        return f'<Loan {self.id}: {self.book.title} - {self.user.username}>'

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    reserved_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, fulfilled, cancelled
    notes = db.Column(db.Text)
    
    def is_expired(self):
        """Check if reservation has expired"""
        return self.expires_at < datetime.utcnow()
    
    def fulfill(self):
        """Fulfill reservation by creating a loan"""
        if self.status == 'pending' and not self.is_expired():
            loan = Loan(
                user_id=self.user_id,
                book_id=self.book_id,
                due_date=datetime.utcnow() + timedelta(days=current_app.config['LOAN_PERIOD_DAYS'])
            )
            self.status = 'fulfilled'
            self.book.available -= 1
            db.session.add(loan)
            return True
        return False
    
    def cancel(self):
        """Cancel reservation"""
        if self.status == 'pending':
            self.status = 'cancelled'
            return True
        return False
    
    def __repr__(self):
        return f'<Reservation {self.id}: {self.book.title} - {self.user.username}>' 