from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120),
                      unique=True,
                      nullable=False)

    password = db.Column(db.String(200),
                         nullable=False)

    enrollments = db.relationship(
        'Enrollment',
        backref='user',
        lazy=True
    )


class Course(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)

    course_name = db.Column(
        db.String(150),
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    duration = db.Column(
        db.String(50)
    )

    description = db.Column(
        db.Text
    )

    enrollments = db.relationship(
        'Enrollment',
        backref='course',
        lazy=True
    )


class Enrollment(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('course.id')
    )

    progress = db.Column(
        db.Integer,
        default=0
    )

    enrollment_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )