from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.decorators.decorators import role_required
from app.models.user import User
from app.models.db import db
from app.models import UpcomingCollection, RecyclingTracker
from app.forms import RegistrationForm as UserForm

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/users", methods=["GET"])
@login_required
@role_required("admin")
def view_users():
    users = User.query.all()
    return render_template("admin/users.html", users=users)


@admin_bp.route("/users/add", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            names=form.names.data,
            email=form.email.data,
            password=form.password.data,
            role=form.role.data,
            address=form.address.data,
        )
        db.session.add(user)
        db.session.commit()
        flash("User added successfully.", "success")
        return redirect(url_for("admin.view_users"))
    return render_template("admin/add_user.html", form=form)


@admin_bp.route("/users/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.names = form.names.data
        user.email = form.email.data
        user.role = form.role.data
        user.address = form.address.data
        db.session.commit()
        flash("User updated successfully.", "success")
        return redirect(url_for("admin.view_users"))
    return render_template("admin/edit_user.html", form=form, user=user)


@admin_bp.route("/users/delete/<int:user_id>", methods=["GET"])
@login_required
@role_required("admin")
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.", "success")
    return redirect(url_for("admin.view_users"))


@admin_bp.route("/analytics", methods=["GET"])
@login_required
@role_required("admin")
def view_analytics():
    total_waste_collected = (
        db.session.query(db.func.sum(RecyclingTracker.quantity)).scalar() or 0
    )
    total_completed_schedules = UpcomingCollection.query.filter_by(
        status="Completed"
    ).count()
    total_cancelled_schedules = UpcomingCollection.query.filter_by(
        status="Cancelled"
    ).count()
    total_users = User.query.count()
    average_impact_score = (
        db.session.query(db.func.avg(RecyclingTracker.impact_score)).scalar() or 0
    )
    average_impact_score = round(average_impact_score, 2)
    tracks = RecyclingTracker.query.all()

    return render_template(
        "admin/analytics.html",
        total_waste_collected=total_waste_collected,
        total_completed_schedules=total_completed_schedules,
        total_cancelled_schedules=total_cancelled_schedules,
        total_users=total_users,
        average_impact_score=average_impact_score,
        tracks=tracks,
    )
