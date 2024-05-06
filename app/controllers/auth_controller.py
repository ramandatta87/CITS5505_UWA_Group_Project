from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.user import User
from app.forms import RegisterForm
from app import db

auth = Blueprint('auth', __name__)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        existing_user = User.query.filter((User.email == form.email.data) | (User.uwa_id == form.uwa_id.data)).first()
        if existing_user is None:
            new_user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                uwa_id=form.uwa_id.data,
                email=form.email.data,
                major=form.major.data
            )
            new_user.set_password(form.password.data)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! You can now login.', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                db.session.rollback()
                flash("Failed to register the user.", "error")
        else:
            flash('Email or UWA ID already exists.', 'error')
    return render_template("register.html", form=form)

@auth.route("/login")
def login():
    return render_template("login.html")
