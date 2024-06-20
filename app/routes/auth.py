from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import RegistrationForm, LoginForm
from app.models.user import User
from app.models.db import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            if user.role == "admin":
                return redirect(url_for("admin.view_analytics"))
            elif user.role == "house-hold":
                return redirect(url_for("user.schedule"))
            elif user.role == "service-man":
                return redirect(url_for("service.view_collections"))
            else:
                flash("Invalid role", "danger")
        flash("Invalid email or password", "danger")
    return render_template("login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            names=form.names.data,
            email=form.email.data,
            password_hash=hashed_password,
            address=form.address.data,
            role=form.role.data,
        )
        print(form.role.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
