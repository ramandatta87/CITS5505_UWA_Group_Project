# Import necessary modules and functions
from datetime import datetime
from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.models.user import User    # Importing the User model
from app.forms import RegisterForm, LoginForm, ForgetPasswordForm  # Importing the RegisterForm
from app import db                  # Importing the database instance


# Define a Blueprint named 'auth' for organizing authentication-related routes and views
auth = Blueprint('auth', __name__)

# Route decorator to map the URL "/register" to the register function
@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # Check if the user already exists based on email or UWA ID
        existing_user = User.query.filter((User.email == form.email.data) | (User.uwa_id == form.uwa_id.data)).first()
        if existing_user is None:  # If user does not exist
            # Create a new user instance with form data, including defaults for new fields
            new_user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                uwa_id=form.uwa_id.data,
                email=form.email.data,
                major=form.major.data,
                is_disabled=False,  # Default value as specified
                timestamp=datetime.utcnow(),  # Current UTC time as timestamp
                role='user'  # Default role
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
                flash(f"Failed to register the user due to {e}", "error")
        else:
            flash('Email or UWA ID already exists.', 'error')
    return render_template("register.html", form=form)


# Route decorator to map the URL "/login" to the login function
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['logged_in'] = True  # Set session variable to indicate the user is logged in
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.index'))  # Assuming 'main' is your Blueprint for index
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    session.pop('logged_in', None)  # Remove 'logged_in' from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))  # Redirect to the index page

@auth.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        # Send reset password instructions
        flash('Please check your email for reset password instructions.')
        return redirect(url_for('auth.login'))
    return render_template('forget_password.html', form=form)

@auth.route('/profile')
def profile():
    # Ensure the user is logged in
    if 'logged_in' in session and session['logged_in']:
        # Logic to show user profile
        return render_template('profile.html')
    else:
        flash("Please log in to view this page.", "warning")
        return redirect(url_for('auth.login'))
    
@auth.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if not session.get('logged_in'):
        flash("Please log in to access this page.", "info")
        return redirect(url_for('auth.login'))
    
    form = ChangePasswordForm()  # Assuming you have a form for changing password
    if form.validate_on_submit():
        # Assuming you have access to current_user or similar
        current_user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('change_password.html', form=form)