# Library Management System

A modern, user-friendly library management system built with Flask, featuring a beautiful UI and comprehensive functionality for managing books, users, and library operations.

![Library Management System](app/static/images/library-dashboard.png)

## Features

### For Users
- 📚 Browse and search books
- 🔍 Advanced filtering by category, author, and availability
- 📖 View detailed book information
- 🔒 Secure user authentication
- 📱 Responsive design for all devices
- 📊 Personal dashboard with reading history
- 📅 Book reservation system

### For Librarians
- 📝 Add and edit books
- 👥 Manage user accounts
- 📊 Generate reports and statistics
- 📋 Track book loans and returns
- 🏷️ Manage categories and authors

### For Administrators
- ⚙️ System configuration
- 📈 Advanced analytics
- 🔐 User role management
- 📊 Comprehensive reporting
- 🔄 System maintenance tools

## Screenshots

### Home Page
![Home Page](app/static/images/home-page.png)

### Book List
![Book List](app/static/images/book-list.png)

### Book Details
![Book Details](app/static/images/book-details.png)

### User Dashboard
![User Dashboard](app/static/images/user-dashboard.png)

### Admin Dashboard
![Admin Dashboard](app/static/images/admin-dashboard.png)

## Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLAlchemy, SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Poppins)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/TeomanV/Library-Management-System-Project.git
cd Library-Management-System-Project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following content:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///library.db
```

5. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

6. Create an admin user:
```bash
python create_admin.py
```

7. Run the application:
```bash
python run.py
```

## Default Admin Credentials

- **Username**: admin
- **Password**: admin123

## Project Structure

```
libraryManagement/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── forms/
│   ├── static/
│   └── templates/
├── migrations/
├── venv/
├── .env
├── .gitignore
├── config.py
├── create_admin.py
├── requirements.txt
└── run.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Teoman V.

## Acknowledgments

- Flask documentation and community
- Bootstrap team for the amazing UI framework
- Font Awesome for the icons
- Google Fonts for the Poppins font family 