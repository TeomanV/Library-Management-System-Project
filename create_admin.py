from app import create_app, db
from app.models.user import User

app = create_app()

def reset_admin_password():
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        
        # Find admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Admin user not found!")
            return
        
        # Reset password
        admin.set_password('admin123')
        db.session.commit()
        
        print("Admin password reset successfully!")
        print("Username: admin")
        print("New Password: admin123")

if __name__ == '__main__':
    reset_admin_password() 