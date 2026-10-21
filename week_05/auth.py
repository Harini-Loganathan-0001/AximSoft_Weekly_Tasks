
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User
from forms import RegisterForm, LoginForm


# AUTHENTICATION BLUEPRINT
auth = Blueprint("auth", __name__)


# =========================
# REGISTER
# =========================
@auth.route("/register", methods=["GET", "POST"])
def register():

    # If already logged in, go to home page
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegisterForm()

    if form.validate_on_submit():

        email = form.email.data.strip().lower()

        # Check whether email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("This email is already registered.", "warning")
            return render_template("register.html", form=form)

        # Create new user
        user = User(
            name=form.name.data.strip(),
            email=email,
            password=generate_password_hash(form.password.data),
            role=form.role.data
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


# =========================
# LOGIN
# =========================
@auth.route("/login", methods=["GET", "POST"])
def login():

    # If already logged in, go to home page
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()

    if form.validate_on_submit():

        email = form.email.data.strip().lower()

        # Find user by email
        user = User.query.filter_by(email=email).first()

        # Verify password
        if user and check_password_hash(
            user.password,
            form.password.data
        ):

            login_user(user)

            flash("Login successful!", "success")

            # Redirect based on user role
            if user.role == "Employer":
                return redirect(url_for("main.employer_dashboard"))

            return redirect(url_for("main.candidate_dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)


# =========================
# LOGOUT
# =========================
@auth.route("/logout", methods=["GET", "POST"])
def logout():

    if current_user.is_authenticated:
        logout_user()

    flash("You have been logged out.", "success")

    return redirect(url_for("main.home"))
