# 🎓 Online Course Management System

A modern **Online Course Management System** built with **Flask**, **SQLite**, **Bootstrap 5**, and **Flask-Login**. The application allows users to register, log in, browse available courses, enroll in courses, track learning progress, and manage their profile.

---

## 📌 Project Overview

The Online Course Management System is a web application that provides a simple learning platform where students can:

- Create an account
- Securely log in
- Browse available courses
- Search courses
- Enroll in courses
- Track course completion progress
- View enrolled courses
- View personal learning statistics

This project demonstrates the fundamentals of **Flask Web Development**, **SQLAlchemy ORM**, **Authentication**, **Database Relationships**, and **Responsive UI Design**.

---

## 🚀 Features

### 👤 User Authentication
- User Registration
- User Login
- User Logout
- Password Hashing
- Session Management

### 📚 Course Management
- View all available courses
- Search courses
- Course descriptions
- Course categories
- Course duration

### ✅ Enrollment System
- Enroll in courses
- Prevent duplicate enrollment
- View enrolled courses

### 📈 Progress Tracking
- Update learning progress
- Progress percentage
- Maximum progress: 100%

### 👤 User Profile
- Total enrolled courses
- Completed courses
- Learning statistics

### 🎨 User Interface
- Responsive Bootstrap Design
- Clean Navigation
- Flash Messages
- Attractive Cards
- Search Bar

---

# 🛠️ Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Programming Language |
| Flask | Web Framework |
| Flask-Login | Authentication |
| Flask-SQLAlchemy | Database ORM |
| Flask-WTF | Forms |
| SQLite | Database |
| Bootstrap 5 | Frontend UI |
| HTML5 | Structure |
| CSS3 | Styling |
| Jinja2 | Template Engine |
| Werkzeug | Password Hashing |

---

# 📂 Project Structure

```
online-course/
│
├── app.py
├── config.py
├── models.py
├── forms.py
├── requirements.txt
│
├── instance/
│   └── courses.db
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
│       └── learnitix.png
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── logout.html
│   ├── register.html
│   ├── courses.html
│   ├── course_detail.html
│   ├── my_courses.html
│   └── profile.html
│
└── README.md
```

---

# 🗄️ Database Schema

## User

| Field | Type |
|--------|------|
| id | Integer |
| name | String |
| email | String |
| password | String |

---

## Course

| Field | Type |
|--------|------|
| id | Integer |
| course_name | String |
| category | String |
| duration | String |
| description | Text |

---

## Enrollment

| Field | Type |
|--------|------|
| id | Integer |
| user_id | Foreign Key |
| course_id | Foreign Key |
| progress | Integer |
| enrollment_date | DateTime |

---

# 🔄 Application Workflow

```
Home
   │
   ▼
Register
   │
   ▼
Login
   │
   ▼
Browse Courses
   │
   ▼
Search Courses
   │
   ▼
Enroll
   │
   ▼
My Courses
   │
   ▼
Update Progress
   │
   ▼
Profile
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/online-course-management.git
```

---

## 2. Move to Project Folder

```bash
cd online-course-management
```

---

## 3. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Run Application

```bash
python app.py
```

---

## 6. Open Browser

```
http://127.0.0.1:5001
```

---

# 🔐 Authentication

Passwords are securely stored using:

- `generate_password_hash()`
- `check_password_hash()`

This ensures user passwords are never stored as plain text.

---

# 📊 Future Enhancements

- Admin Dashboard
- Instructor Panel
- Course Videos
- Quiz System
- Certificate Generation
- Course Reviews
- Payment Integration
- Email Verification
- Password Reset
- Profile Picture Upload
- Pagination
- Course Completion Certificates
- Dashboard Analytics

---

# 📷 Screenshots

Add screenshots here after uploading your project.

Example:

```
screenshots/
├── home.png
├── login.png
├── register.png
├── courses.png
├── profile.png
```

---

# 🎯 Learning Outcomes

This project helped in understanding:

- Flask Routing
- Flask Templates (Jinja2)
- SQLAlchemy Models
- Database Relationships
- CRUD Operations
- User Authentication
- Password Hashing
- Bootstrap UI Development
- Session Management
- Flash Messages
- Search Functionality

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

# 📄 License

This project is developed for educational purposes.

---

# 👨‍💻 Author

**Bayy**

Software Trainee

GitHub: https://github.com/yourusername

LinkedIn: https://linkedin.com/in/yourprofile
