from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import request

from config import Config
from models import db
from models import User
from models import Course
from models import Enrollment

from flask_login import LoginManager
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():

    db.create_all()

    if Course.query.count() == 0:

        courses = [

    Course(
        course_name="Python Programming",
        category="Programming",
        duration="8 Weeks",
        description="Learn Python from beginner to advanced."
    ),

    Course(
        course_name="Flask Development",
        category="Web Development",
        duration="6 Weeks",
        description="Build web applications using Flask."
    ),

    Course(
        course_name="SQL Database",
        category="Database",
        duration="4 Weeks",
        description="Master SQL queries and database design."
    ),

    Course(
        course_name="Java Programming",
        category="Programming",
        duration="8 Weeks",
        description="Learn object-oriented programming with Java."
    ),

    Course(
        course_name="C Programming",
        category="Programming",
        duration="6 Weeks",
        description="Understand programming fundamentals using C."
    ),

    Course(
        course_name="C++ Programming",
        category="Programming",
        duration="8 Weeks",
        description="Build efficient applications using C++."
    ),

    Course(
        course_name="JavaScript Essentials",
        category="Web Development",
        duration="5 Weeks",
        description="Learn JavaScript for interactive websites."
    ),

    Course(
        course_name="HTML & CSS",
        category="Web Development",
        duration="4 Weeks",
        description="Create responsive web pages from scratch."
    ),

    Course(
        course_name="React JS",
        category="Web Development",
        duration="6 Weeks",
        description="Develop modern frontend applications."
    ),

    Course(
        course_name="Node.js Development",
        category="Web Development",
        duration="6 Weeks",
        description="Build backend applications with Node.js."
    ),

    Course(
        course_name="Django Framework",
        category="Web Development",
        duration="7 Weeks",
        description="Create powerful web apps using Django."
    ),

    Course(
        course_name="Data Structures",
        category="Computer Science",
        duration="6 Weeks",
        description="Learn arrays, stacks, queues, trees, and graphs."
    ),

    Course(
        course_name="Algorithms",
        category="Computer Science",
        duration="6 Weeks",
        description="Master problem-solving and optimization techniques."
    ),

    Course(
        course_name="Machine Learning",
        category="Artificial Intelligence",
        duration="10 Weeks",
        description="Build predictive models using ML algorithms."
    ),

    Course(
        course_name="Deep Learning",
        category="Artificial Intelligence",
        duration="10 Weeks",
        description="Learn neural networks and deep learning concepts."
    ),

    Course(
        course_name="Artificial Intelligence",
        category="Artificial Intelligence",
        duration="8 Weeks",
        description="Introduction to AI concepts and applications."
    ),

    Course(
        course_name="Data Science",
        category="Data Analytics",
        duration="8 Weeks",
        description="Analyze and visualize data effectively."
    ),

    Course(
        course_name="Power BI",
        category="Data Analytics",
        duration="4 Weeks",
        description="Create interactive business dashboards."
    ),

    Course(
        course_name="Excel for Data Analysis",
        category="Data Analytics",
        duration="3 Weeks",
        description="Analyze business data using Excel."
    ),

    Course(
        course_name="Cloud Computing",
        category="Cloud",
        duration="8 Weeks",
        description="Learn cloud concepts and services."
    ),

    Course(
        course_name="AWS Fundamentals",
        category="Cloud",
        duration="6 Weeks",
        description="Understand AWS core services and deployment."
    ),

    Course(
        course_name="Cyber Security",
        category="Security",
        duration="8 Weeks",
        description="Protect systems from cyber threats."
    ),

    Course(
        course_name="Ethical Hacking",
        category="Security",
        duration="8 Weeks",
        description="Learn penetration testing and security auditing."
    ),

    Course(
        course_name="Mobile App Development",
        category="Mobile Development",
        duration="8 Weeks",
        description="Build Android applications from scratch."
    ),

    Course(
        course_name="Flutter Development",
        category="Mobile Development",
        duration="7 Weeks",
        description="Create cross-platform mobile applications."
    ),

    Course(
        course_name="Software Testing",
        category="Software Engineering",
        duration="5 Weeks",
        description="Learn manual and automated testing techniques."
    ),

    Course(
        course_name="DevOps",
        category="Software Engineering",
        duration="6 Weeks",
        description="Implement CI/CD and deployment pipelines."
    ),

    Course(
        course_name="Git & GitHub",
        category="Tools",
        duration="3 Weeks",
        description="Version control and collaboration using Git."
    ),

    Course(
        course_name="UI/UX Design",
        category="Design",
        duration="6 Weeks",
        description="Design user-friendly digital products."
    ),

    Course(
        course_name="Blockchain Basics",
        category="Emerging Technologies",
        duration="5 Weeks",
        description="Understand blockchain technology and applications."
    )

]

        db.session.add_all(courses)
        db.session.commit()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            flash("Email already exists")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(
            password
        )

        user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login Successful", "success")
            return redirect(url_for("courses"))   # redirect instead of render
        else:
            flash("Invalid Email or Password", "danger")

    return render_template("login.html")



@app.route("/logout")
def logout():
    logout_user()
    # Instead of flashing and redirecting, render logout.html
    return render_template("logout.html")

@app.route("/courses")
@login_required
def courses():

    search = request.args.get("search", "")

    if search:
        all_courses = Course.query.filter(
            Course.course_name.ilike(f"%{search}%")
        ).all()
    else:
        all_courses = Course.query.all()

    enrolled_courses = [
        enrollment.course_id
        for enrollment in Enrollment.query.filter_by(user_id=current_user.id).all()
    ]

    print("Current User:", current_user.id)
    print("Enrolled Courses:", enrolled_courses)

    return render_template(
        "courses.html",
        courses=all_courses,
        search=search,
        enrolled_courses=enrolled_courses
    )

@app.route("/enroll/<int:id>")
@login_required
def enroll(id):

    existing_enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=id
    ).first()

    if existing_enrollment:
        flash("Already Enrolled")
        return redirect(url_for("my_courses"))

    enrollment = Enrollment(
        user_id=current_user.id,
        course_id=id,
        progress=0
    )

    db.session.add(enrollment)
    db.session.commit()

    flash("Enrolled Successfully")

    return redirect(
        url_for("my_courses")
    )


@app.route("/my-courses")
def my_courses():
    if not current_user.is_authenticated:
        flash("Please log in to view your enrolled courses", "info")
        return redirect(url_for("login"))

    enrollments = Enrollment.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "my_courses.html",
        enrollments=enrollments
    )


@app.route("/update-progress/<int:id>")
@login_required
def update_progress(id):

    enrollment = Enrollment.query.get(id)

    if enrollment:

        if enrollment.progress < 100:
            enrollment.progress += 10

        db.session.commit()

    return redirect(
        url_for("my_courses")
    )


@app.route("/profile")
def profile():
    if not current_user.is_authenticated:
        flash("Please log in to access your profile", "info")
        return redirect(url_for("login"))

    total_courses = Enrollment.query.filter_by(
        user_id=current_user.id
    ).count()

    completed_courses = Enrollment.query.filter_by(
        user_id=current_user.id,
        progress=100
    ).count()

    return render_template(
        "profile.html",
        total_courses=total_courses,
        completed_courses=completed_courses
    )

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = None  # disable default message

@login_manager.unauthorized_handler
def unauthorized():
    # Different message depending on route
    from flask import request
    if request.path == "/my-courses":
        flash("Please log in to view your enrolled courses.", "warning")
    elif request.path == "/profile":
        flash("Please log in to access your profile.", "warning")
    else:
        flash("Please log in to continue.", "warning")
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
