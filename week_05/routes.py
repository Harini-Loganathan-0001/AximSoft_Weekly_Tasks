import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename
from sqlalchemy import or_

from models import db, Job, Application, User
from models import SavedJob
from forms import JobForm, ProfileForm

main = Blueprint("main", __name__)



# HOME

@main.route("/")
def home():
    return render_template("index.html")


# JOB LISTING + SEARCH

@main.route("/jobs")
def jobs():

    search = request.args.get("search", "")
    experience = request.args.get("experience", "")
    job_type = request.args.get("job_type", "")

    jobs_query = Job.query.join(User)

    if search:
        jobs_query = jobs_query.filter(
            or_(
                Job.job_title.ilike(f"%{search}%"),
                User.company_name.ilike(f"%{search}%"),
                Job.location.ilike(f"%{search}%")
            )
        )

    if experience:
        jobs_query = jobs_query.filter(Job.experience == experience)

    if job_type:
        jobs_query = jobs_query.filter(Job.job_type == job_type)

    jobs = jobs_query.order_by(Job.posted_date.desc()).all()

    return render_template("jobs.html", jobs=jobs)



# JOB DETAILS

@main.route("/job/<int:job_id>")
def job_details(job_id):

    job = Job.query.get_or_404(job_id)

    return render_template("job_details.html", job=job)


# APPLY JOB

@main.route("/apply/<int:job_id>", methods=["POST"])
@login_required
def apply_job(job_id):

    if current_user.role != "Candidate":
        flash("Only candidates can apply for jobs.", "danger")
        return redirect(url_for("main.jobs"))
    
    # Check if profile is updated (you can decide which fields are mandatory)
    if not current_user.phone or not current_user.education or not current_user.resume:
        flash("Please update your profile with phone, education, and resume before applying.", "warning")
        return redirect(url_for("main.edit_profile"))

    job = Job.query.get_or_404(job_id)

    existing = Application.query.filter_by(
        user_id=current_user.id,
        job_id=job.id
    ).first()

    if existing:
        flash("You have already applied for this job.", "warning")
        return redirect(url_for("main.job_details", job_id=job.id))

    application = Application(
        user_id=current_user.id,
        job_id=job.id,
        status="Pending"
    )

    db.session.add(application)
    db.session.commit()

    flash("Application submitted successfully!", "success")

    return redirect(url_for("main.job_details", job_id=job.id))



# CANDIDATE DASHBOARD

@main.route("/candidate/dashboard")
@login_required
def candidate_dashboard():

    if current_user.role != "Candidate":
        flash("Access denied.", "danger")
        return redirect(url_for("main.home"))

    applications = Application.query.filter_by(
        user_id=current_user.id
    ).order_by(Application.applied_date.desc()).all()

    saved_jobs = SavedJob.query.filter_by(
        user_id=current_user.id
    ).order_by(SavedJob.saved_date.desc()).all()

    # Dashboard summary counts
    total_applied = len(applications)
    total_pending = Application.query.filter_by(
        user_id=current_user.id, status="Pending"
    ).count()
    total_interviews = Application.query.filter_by(
        user_id=current_user.id, status="Interviewing"
    ).count()
    total_saved = len(saved_jobs)

    return render_template(
        "candidate/dashboard.html",
        applications=applications,
        saved_jobs=saved_jobs,
        total_applied=total_applied,
        total_pending=total_pending,
        total_interviews=total_interviews,
        total_saved=total_saved
    )




# EMPLOYER DASHBOARD

@main.route("/employer/dashboard")
@login_required
def employer_dashboard():

    if current_user.role != "Employer":
        flash("Access denied.", "danger")
        return redirect(url_for("main.home"))

    jobs = Job.query.filter_by(
        employer_id=current_user.id
    ).order_by(Job.posted_date.desc()).all()

    total_applications = Application.query.join(Job).filter(
        Job.employer_id == current_user.id
    ).count()

    total_interviews = Application.query.join(Job).filter(
        Job.employer_id == current_user.id,
        Application.status == "Interviewing"
    ).count()

    total_hires = Application.query.join(Job).filter(
        Job.employer_id == current_user.id,
        Application.status == "Hired"
    ).count()

    return render_template(
        "employer/dashboard.html",
        jobs=jobs,
        total_jobs=len(jobs),
        total_applications=total_applications,
        total_interviews=total_interviews,
        total_hires=total_hires

    )


# PROFILE (CANDIDATE)


@main.route("/profile", methods=["GET"])
@login_required
def profile():

    if current_user.role != "Candidate":
        flash("Access denied.", "danger")
        return redirect(url_for("main.home"))

    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():

        current_user.phone = form.phone.data
        current_user.city = form.city.data
        current_user.skills = form.skills.data
        current_user.experience = form.experience.data
        current_user.education = form.education.data
        current_user.about = form.about.data

        # Profile picture upload
        if form.profile_pic.data:
            filename = secure_filename(form.profile_pic.data.filename)
            path = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "profiles",
                filename
            )
            form.profile_pic.data.save(path)
            current_user.profile_pic = filename

        # Resume upload
        if form.resume.data:
            filename = secure_filename(form.resume.data.filename)
            path = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "resumes",
                filename
            )
            form.resume.data.save(path)
            current_user.resume = filename

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("main.profile"))

    return render_template("candidate/profile.html", form=form)




# EDIT PROFILE (CANDIDATE)

@main.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():

    if current_user.role != "Candidate":
        flash("Access denied.", "danger")
        return redirect(url_for("main.home"))

    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():

        current_user.phone = form.phone.data
        current_user.city = form.city.data
        current_user.skills = form.skills.data
        current_user.experience = form.experience.data
        current_user.education = form.education.data
        current_user.about = form.about.data

        # Profile picture upload (only if a new file is selected)
        if form.profile_pic.data and hasattr(form.profile_pic.data, "filename") and form.profile_pic.data.filename != "":
            filename = secure_filename(form.profile_pic.data.filename)
            path = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "profiles",
                filename
            )
            form.profile_pic.data.save(path)
            current_user.profile_pic = filename

        # Resume upload (only if a new file is selected)
        if form.resume.data and hasattr(form.resume.data, "filename") and form.resume.data.filename != "":
            filename = secure_filename(form.resume.data.filename)
            path = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "resumes",
                filename
            )
            form.resume.data.save(path)
            current_user.resume = filename


        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("main.profile"))

    return render_template("candidate/edit_profile.html", form=form)




# POST JOB

@main.route("/post-job", methods=["GET", "POST"])
@login_required
def post_job():

    if current_user.role != "Employer":
        flash("Only employers can post jobs.", "danger")
        return redirect(url_for("main.home"))

    # Check if company profile is filled
    if not current_user.company_name or not current_user.company_location:
        flash("⚠️ Please complete your Company Profile before posting a job.", "warning")
        return redirect(url_for("main.company_profile"))  # redirect to profile page

    form = JobForm()

    if form.validate_on_submit():

        job = Job(
            job_title=form.job_title.data,
            location=form.location.data,
            experience=form.experience.data,
            salary=form.salary.data,
            job_type=form.job_type.data,
            skills=form.skills.data,
            description=form.description.data,
            employer_id=current_user.id
        )

        db.session.add(job)
        db.session.commit()

        flash("Job posted successfully!", "success")
        return redirect(url_for("main.jobs"))

    return render_template("employer/add_job.html", form=form)


# EDIT JOB

@main.route("/edit-job/<int:job_id>", methods=["GET", "POST"])
@login_required
def edit_job(job_id):

    job = Job.query.get_or_404(job_id)

    if job.employer_id != current_user.id:
        abort(403)

    form = JobForm(obj=job)

    if form.validate_on_submit():

        form.populate_obj(job)
        db.session.commit()

        flash("Job updated successfully.", "success")
        return redirect(url_for("main.employer_dashboard"))

    return render_template("employer/edit_job.html", form=form, job=job)



# DELETE JOB

@main.route("/delete-job/<int:job_id>", methods=["POST"])
@login_required
def delete_job(job_id):

    job = Job.query.get_or_404(job_id)

    if job.employer_id != current_user.id:
        abort(403)

    db.session.delete(job)
    db.session.commit()

    flash("Job deleted successfully!", "success")
    return redirect(url_for("main.employer_dashboard"))



# VIEW APPLICANTS

@main.route("/applicants/<int:job_id>")
@login_required
def view_applicants(job_id):

    job = Job.query.get_or_404(job_id)

    if job.employer_id != current_user.id:
        flash("Access denied.", "danger")
        return redirect(url_for("main.employer_dashboard"))

    applications = Application.query.filter_by(job_id=job.id).all()

    return render_template(
        "employer/applicants.html",
        job=job,
        applications=applications
    )


# =========================
# UPDATE STATUS
# =========================
@main.route("/update-status/<int:app_id>/<status>")
@login_required
def update_status(app_id, status):

    application = Application.query.get_or_404(app_id)

    if application.job.employer_id != current_user.id:
        flash("Access denied.", "danger")
        return redirect(url_for("main.employer_dashboard"))

    allowed_status = ["Pending", "In Review", "Interviewing", "Hired", "Rejected"]

    if status not in allowed_status:
        flash("Invalid status.", "danger")
        return redirect(url_for("main.view_applicants", job_id=application.job_id))

    # Prevent changing an already hired application
    if application.status == "Hired":
        flash("Candidate is already hired. Status cannot be changed.", "warning")
        return redirect(url_for("main.view_applicants", job_id=application.job_id))

    # Check if this candidate is already hired by this employer
    if status == "Hired":

        already_hired = Application.query.join(Job).filter(
            Application.user_id == application.user_id,
            Application.status == "Hired",
            Job.employer_id == current_user.id,
            Application.id != application.id
        ).first()

        if already_hired:
            flash("This candidate is already hired by your company.", "warning")
            return redirect(url_for("main.view_applicants", job_id=application.job_id))
            

    application.status = status
    db.session.commit()

    flash("Status updated successfully!", "success")

    return redirect(url_for("main.view_applicants", job_id=application.job_id))



# COMPANY PROFILE (NEW - IMPORTANT)

@main.route("/company-profile", methods=["GET", "POST"])
@login_required
def company_profile():

    if current_user.role != "Employer":
        flash("Access denied.", "danger")
        return redirect(url_for("main.home"))

    if request.method == "POST":

        current_user.company_name = request.form.get("company_name")
        current_user.company_website = request.form.get("company_website")
        current_user.industry = request.form.get("industry")
        current_user.company_size = request.form.get("company_size")
        current_user.founded = request.form.get("founded")
        current_user.company_location = request.form.get("company_location")
        current_user.company_about = request.form.get("company_about")

        # Logo upload
        if "company_logo" in request.files:
            file = request.files["company_logo"]

            if file.filename != "":
                filename = secure_filename(file.filename)
                path = os.path.join(current_app.root_path, "static", "uploads", filename)
                file.save(path)

                current_user.company_logo = filename

        db.session.commit()

        flash("Company profile updated successfully!", "success")
        return redirect(url_for("main.company_profile"))

    return render_template("employer/company_profile.html")

# Check if edit mode is requested
    edit_mode = request.args.get("edit")
    return render_template("employer/company_profile.html", user=current_user, edit=edit_mode)


@main.route("/view-resume/<int:app_id>")
@login_required
def view_resume(app_id):

    application = Application.query.get_or_404(app_id)

    # Allow only the employer who owns the job
    if application.job.employer_id != current_user.id:
        flash("Access denied.", "danger")
        return redirect(url_for("main.employer_dashboard"))

    return render_template("view_resume.html", application=application)
# Saving Jobs

@main.route("/save-job/<int:job_id>", methods=["POST"])
@login_required
def save_job(job_id):

    if current_user.role != "Candidate":
        flash("Only candidates can save jobs.", "danger")
        return redirect(request.referrer or url_for("main.jobs"))

    job = Job.query.get_or_404(job_id)

    existing = SavedJob.query.filter_by(
        user_id=current_user.id,
        job_id=job.id
    ).first()

    if existing:
        flash("Job already saved.", "warning")
        return redirect(url_for("main.jobs"))

    saved = SavedJob(user_id=current_user.id, job_id=job.id)

    db.session.add(saved)
    db.session.commit()

    flash("Job saved successfully!", "success")
    return redirect(url_for("main.jobs"))

#unsave
@main.route("/unsave-job/<int:job_id>", methods=["POST"])
@login_required
def unsave_job(job_id):

    saved = SavedJob.query.filter_by(
        user_id=current_user.id,
        job_id=job_id
    ).first()

    if saved:
        db.session.delete(saved)
        db.session.commit()
        flash("Job removed from saved list.", "success")

    return redirect(request.referrer or url_for("main.jobs"))