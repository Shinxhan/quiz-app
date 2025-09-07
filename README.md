# 📚 Quiz App - Django Web Application

A comprehensive web-based quiz platform built with Django, featuring user authentication, quiz management, and administrative tools for educational institutions and training programs.

## ✨ Features

### For Users
- 🔐 **User Registration & Authentication** - Secure login/logout system
- 📋 **Category-Based Quizzes** - Browse quizzes organized by categories
- ⏱️ **Timed Quiz Sessions** - JavaScript-based timer with auto-submission
- 📊 **Progress Tracking** - View your quiz attempts and scores
- 🎯 **Interactive Quiz Interface** - Clean, responsive design with Bootstrap

### For Administrators
- 🎛️ **Admin Dashboard** - Overview of users, quizzes, and attempts
- 📝 **Quiz Management** - Create, edit, delete quizzes with status control
- 👥 **User Management** - Add, edit, and manage user accounts
- 📤 **CSV Import** - Bulk upload quizzes and users via CSV files
- 🔧 **Django Admin Integration** - Full backend administration panel

## 🛠️ Technology Stack

- **Backend:** Django 5.2.4
- **Database:** SQLite3 (Development)
- **Frontend:** HTML5, CSS3, Bootstrap 4.5.2, JavaScript
- **Authentication:** Django's built-in user system
- **Session Management:** Django sessions for quiz state

## 📁 Project Structure

```
quiz_app/
├── quiz_project/          # Main Django project
│   ├── settings.py        # Project configuration
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI configuration
├── core/                  # Main application
│   ├── models.py         # Data models
│   ├── views.py          # View controllers
│   ├── admin.py          # Admin configuration
│   └── apps.py           # App configuration
├── templates/core/        # HTML templates
├── static/               # CSS, JS, and media files
├── venv/                 # Virtual environment
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd quiz_app
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main app: http://127.0.0.1:8000/
   - Admin dashboard: http://127.0.0.1:8000/admin/dashboard/
   - Django admin: http://127.0.0.1:8000/admin/

## 📖 Usage Guide

### Creating Your First Quiz

1. **Login as admin** and navigate to the admin dashboard
2. **Add Categories** - Organize your quizzes by subject/topic
3. **Create Quiz** - Add title, select category, set status
4. **Add Questions** - Use Django admin to add questions and options
5. **Set Status to Active** - Make the quiz available to users

### CSV Import Format

**For Quizzes (quizzes.csv):**
```csv
title,category,status
Python Basics,Programming,active
Web Development,Programming,active
```

**For Users (users.csv):**
```csv
username,email,password
student1,student1@example.com,password123
student2,student2@example.com,password456
```

### Taking a Quiz

1. **Register/Login** as a regular user
2. **Browse Categories** on the home page
3. **Select a Quiz** from the category
4. **Start Quiz** - Session-based progress tracking
5. **Answer Questions** - Navigate through questions
6. **View Results** - See your score and attempt history

## 🏗️ Data Model

```
Category (1) ──→ (Many) Quiz (1) ──→ (Many) Question (1) ──→ (Many) Option
                    │
                    └── (Many) Attempt (1) ──→ (Many) Answer
                             │
                        User (Many) ←──┘
```

### Key Models:
- **Category**: Quiz organization
- **Quiz**: Container for questions with status control
- **Question**: Individual quiz questions
- **Option**: Answer choices (with correct flag)
- **Attempt**: User's quiz session record
- **Answer**: Individual question responses

## 🔧 Configuration

### Environment Variables
The application uses Django's settings.py for configuration. For production:

- Set `DEBUG = False`
- Configure proper database (PostgreSQL/MySQL)
- Set secure `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Setup static files serving

### Quiz Timer
Modify the timer in `templates/core/base.html`:
```javascript
let totalTime = 60;  // seconds per question
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run tests for core app
python manage.py test core

# Run with coverage (if coverage installed)
coverage run manage.py test
coverage report
```

## 📊 Admin Features

### Dashboard Metrics
- Total users count
- Total quizzes count
- Total attempts count
- Top 5 most attempted quizzes

### Management Capabilities
- **Quiz Status Control**: Active, Hold, Disabled
- **Bulk Operations**: CSV import for quizzes and users
- **User Management**: Create, edit, delete user accounts
- **Analytics**: View attempt patterns and quiz performance

## 🔒 Security Features

- **CSRF Protection**: Django's built-in CSRF middleware
- **Password Hashing**: Secure password storage
- **Session Security**: Secure session management
- **Staff Access Control**: Decorator-based permission system
- **Input Validation**: Form validation and sanitization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Issues & Support

If you encounter any issues or have questions:
1. Check the existing issues on GitHub
2. Create a new issue with detailed description
3. Include steps to reproduce the problem

## 🚀 Future Enhancements

- [ ] Question types (multiple choice, true/false, text input)
- [ ] Quiz difficulty levels
- [ ] Time limits per quiz
- [ ] Result analytics and reporting
- [ ] Email notifications
- [ ] API endpoints for mobile app integration
- [ ] Question randomization
- [ ] Quiz categories with icons

---

**Built with ❤️ using Django**
