from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    SubmitField,
    TextAreaField
)

from wtforms.validators import DataRequired, Email, EqualTo

from flask_wtf.file import FileField, FileAllowed



# PROFILE FORM (CANDIDATE)

class ProfileForm(FlaskForm):

    phone = StringField("Phone Number")

    city = StringField("City")

    skills = TextAreaField("Skills")

    experience = StringField("Experience")

    education = StringField("Education")

    about = TextAreaField("About Me")

    profile_pic = FileField(
        "Profile Picture",
        validators=[FileAllowed(["jpg", "jpeg", "png"], "Images only!")]
    )

    resume = FileField(
        "Resume (PDF)",
        validators=[FileAllowed(["pdf"], "PDF only!")]
    )

    submit = SubmitField("Save Profile")



# REGISTER FORM

class RegisterForm(FlaskForm):

    name = StringField("Full Name", validators=[DataRequired()])

    email = StringField("Email", validators=[Email()])

    password = PasswordField("Password", validators=[DataRequired()])

    confirm = PasswordField(
        "Confirm Password",
        validators=[EqualTo("password")]
    )

    role = SelectField(
        "Role",
        choices=[
            ("Candidate", "Candidate"),
            ("Employer", "Employer")
        ]
    )

    submit = SubmitField("Register")



# LOGIN FORM

class LoginForm(FlaskForm):

    email = StringField("Email", validators=[Email()])

    password = PasswordField("Password", validators=[DataRequired()])

    submit = SubmitField("Login")



# JOB FORM 

class JobForm(FlaskForm):

    # company_name REMOVED 

    job_title = StringField(
        "Job Title",
        validators=[DataRequired()]
    )

    location = StringField(
        "Location",
        validators=[DataRequired()]
    )

    experience = SelectField(
        "Experience",
        choices=[
            ("Fresher", "Fresher"),
            ("1-2 Years", "1-2 Years"),
            ("3-5 Years", "3-5 Years"),
            ("5+ Years", "5+ Years")
        ]
    )

    salary = StringField(
        "Salary",
        validators=[DataRequired()]
    )

    job_type = SelectField(
        "Job Type",
        choices=[
            ("Full Time", "Full Time"),
            ("Part Time", "Part Time"),
            ("Internship", "Internship"),
            ("Remote", "Remote")
        ]
    )

    skills = TextAreaField(
        "Skills",
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Job Description",
        validators=[DataRequired()]
    )

    submit = SubmitField("Post Job")