# Import necessary modules and functions
from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.user import User    # Importing the User model
from app.forms import RegisterForm  # Importing the RegisterForm
from app import db                  # Importing the database instance


# Define a Blueprint named 'auth' for organizing authentication-related routes and views
auth = Blueprint('auth', __name__)

# Route decorator to map the URL "/register" to the register function
@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    # Check if the request method is POST and the form data is valid

    if request.method == 'POST' and form.validate():
        # Check if the user already exists based on email or UWA ID
        existing_user = User.query.filter((User.email == form.email.data) | (User.uwa_id == form.uwa_id.data)).first()
        if existing_user is None:   # If user does not exist
            
            # Create a new user instance with form data
            new_user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                uwa_id=form.uwa_id.data,
                email=form.email.data,
                major=form.major.data
            )

            # Set the password for the new user
            new_user.set_password(form.password.data)
            try:
                # Add the new user to the database session and commit changes
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


# Route decorator to map the URL "/login" to the login function
@auth.route("/login")
def login():
    return render_template("login.html")
