
# Job Portal Web Application
 
## Project Overview
 
The Job Portal Web Application is a modern recruitment platform developed using **Python Flask**, **SQLAlchemy**, **Bootstrap 5**, and **SQLite**. It allows employers to post and manage jobs while candidates can search, apply, and track their job applications through a responsive web interface.
 
This project is inspired by platforms like **LinkedIn Jobs**, **Indeed**, and **Naukri**.
 
---
 
## Technologies Used
 
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- SQLite
- Bootstrap 5
- HTML5
- CSS3
- JavaScript
 
---
 
## Features
 
### Authentication
- User Registration
- Secure Login
- Logout
- Role-based Authentication
  - Employer
  - Candidate
 
### Home Page
- Responsive Navigation Bar
- Hero Section
- Featured Companies
- Latest Job Listings
- Job Search
 
### Job Management
- View All Jobs
- Search Jobs
- Filter by Experience
- Filter by Job Type
- View Job Details
 
### Employer Features
- Employer Dashboard
- Post New Job
- Edit Job
- Delete Job
- View Own Posted Jobs Only
- View Applicants
- Update Application Status
  - Pending
  - In Review
  - Interviewing
  - Hired
 
### Candidate Features
- Candidate Dashboard
- Apply for Jobs
- Track Application Status
- View Applied Jobs
 
### Candidate Profile
- Edit Personal Information
- Upload Profile Picture
- Upload Resume (PDF)
- View Profile
- Employer can View Candidate Resume
 
---
 
## Project Structure
 
```
JobPortal/
│
├── static/
│   ├── css/
│   ├── images/
│   ├── js/
│   └── uploads/
│       ├── profiles/
│       └── resumes/
│
├── templates/
│   ├── candidate/
│   ├── employer/
│   ├── base.html
│   ├── index.html
│   ├── jobs.html
│   ├── job_details.html
│   ├── login.html
│   └── register.html
│
├── auth.py
├── routes.py
├── models.py
├── forms.py
├── app.py
├── database.db
└── README.md
```
 
---
 
## Database Tables
 
### User
- Name
- Email
- Password
- Role
- Phone
- City
- Skills
- Experience
- Education
- About
- Profile Picture
- Resume
 
### Job
- Company Name
- Job Title
- Location
- Experience
- Salary
- Job Type
- Skills
- Description
- Posted Date
- Employer ID
 
### Application
- Candidate
- Job
- Applied Date
- Status
 
---
 
## Installation
 
Clone the project
 
```bash
git clone <repository-url>
```
 
Install dependencies
 
```bash
pip install -r requirements.txt
```
 
Run the application
 
```bash
python app.py
```
 
Open your browser
 
```
http://127.0.0.1:5000
```
 
---
 
## User Roles
 
### Employer
- Register as Employer
- Login
- Post Jobs
- Edit Jobs
- Delete Jobs
- View Applicants
- Update Candidate Status
 
### Candidate
- Register as Candidate
- Login
- Search Jobs
- Apply for Jobs
- Update Profile
- Upload Resume
- Track Applications
 
---
 
## Future Enhancements
 
- Company Profile Management
- Saved Jobs
- Email Notifications
- Admin Dashboard
- Job Recommendations
- Interview Scheduling
- Company Logo Upload
- Password Reset
- Pagination
- Advanced Search
 
---
 
## Developed By
 
**Harini Loganathan**
 
Python Flask Assessment Project
