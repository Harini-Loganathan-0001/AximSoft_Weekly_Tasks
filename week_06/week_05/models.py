from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from datetime import datetime

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "auth.login"



# USER MODEL

class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    # Basic Info
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    phone = db.Column(db.String(20))
    city = db.Column(db.String(100))
    skills = db.Column(db.Text)
    experience = db.Column(db.String(100))
    education = db.Column(db.String(100))
    about = db.Column(db.Text)

    profile_pic = db.Column(db.String(100))
    resume = db.Column(db.String(100))

    created = db.Column(db.DateTime, default=datetime.utcnow)

    # COMPANY PROFILE (Employer only)

    company_logo = db.Column(db.String(150))
    company_name = db.Column(db.String(150))
    company_website = db.Column(db.String(150))
    industry = db.Column(db.String(100))
    company_size = db.Column(db.String(100))
    founded = db.Column(db.String(20))
    company_about = db.Column(db.Text)
    company_location = db.Column(db.String(150))

    
    # RELATIONSHIPS
    

    # Employer -> Jobs
    jobs = db.relationship(
        "Job",
        backref="employer",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # Candidate -> Applications
    applications = db.relationship(
        "Application",
        backref="candidate",
        lazy=True,
        cascade="all, delete-orphan"
    )



# JOB MODEL

class Job(db.Model):

    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)

    job_title = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.String(50), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)

    skills = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)

    posted_date = db.Column(db.DateTime, default=datetime.utcnow)

    employer_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    # Job -> Applications
    applications = db.relationship(
        "Application",
        backref="job",
        lazy=True,
        cascade="all, delete-orphan"
    )


class SavedJob(db.Model):
    __tablename__ = "saved_jobs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)

    saved_date = db.Column(db.DateTime, default=db.func.now())

    job = db.relationship('Job', backref='saved_by')
    user = db.relationship('User', backref='saved_jobs')



# APPLICATION MODEL

class Application(db.Model):

    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.id"),
        nullable=False
    )

    applied_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    resume_file = db.Column(db.String(200))



# LOGIN LOADER

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))