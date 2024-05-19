from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from app.model.models import User
from app.View.forms import RegisterForm, LoginForm, ForgetPasswordForm, ChangePasswordForm, EditProfileForm
from app import db, mail
from flask_mail import Message

# Define the auth Blueprint for handling authentication-related routes
auth = Blueprint('auth', __name__)

# Route for user registration
@auth.route("/register", methods=['GET', 'POST'])
def register():
    """
    Route for user registration.
    """
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # Check if user with the provided email or UWA ID already exists
        existing_user = User.query.filter(
            (User.email == form.email.data) | (User.uwa_id == form.uwa_id.data)
        ).first()
        if existing_user is None:
            # Create a new user
            new_user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                uwa_id=form.uwa_id.data,
                email=form.email.data,
                major=form.major.data,
                is_disabled=False,
                timestamp=datetime.utcnow(),
                role='user'
            )
            new_user.set_password(form.password.data)
            try:
                # Add the new user to the database
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! You can now login.', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                # Rollback in case of any error during the database transaction
                db.session.rollback()
                flash(f"Failed to register the user due to {e}", "error")
        else:
            flash('Email or UWA ID already exists.', 'error')
    return render_template("auth/register.html", form=form)

# Route for user login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for user login.
    """
    form = LoginForm()
    if form.validate_on_submit():
        # Check if the user exists and the password is correct
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            session['logged_in'] = True
            session['user_name'] = f"{user.first_name} {user.last_name}"
            session['user_id'] = user.id
            session['server_start_token'] = current_app.config['SERVER_START_TOKEN']
            return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check your email and password.', 'danger')
    return render_template('auth/login.html', form=form)

# Route for user logout
@auth.route('/logout')
def logout():
    """
    Route for user logout.
    """
    session.clear()
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

# Route for forgetting password and resetting it
@auth.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    """
    Route for forgetting password and resetting it.
    """
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        # Fetch the user based on UWA ID and Email for extra verification
        user = User.query.filter_by(uwa_id=form.uwa_id.data, email=form.email.data).first()
        if user and user.first_name == form.first_name.data:
            # Update the user's password
            user.password_hash = generate_password_hash(form.new_password.data)
            db.session.commit()
            send_password_change_email(user)
            flash('Your password has been updated. Please check your email for confirmation.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('auth/forgetpassword.html', form=form)

# Function to send password change confirmation email
def send_password_change_email(user):
    """
    Function to send password change confirmation email.
    """
    msg = Message('Password Change Confirmation', sender='cssedevconnect@gmail.com', recipients=[user.email])
    msg.body = f'''Hello {user.first_name},

This is a confirmation that the password for your account {user.email} has just been changed.

If you did not make this change, please contact support immediately.

Best regards,
CSSE DevConnect
'''
    mail.send(msg)

# Route for changing password
@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    Route to change the user's password.
    """
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.get_or_404(current_user.id)
        if user.check_password(form.old_password.data):
            user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated.', 'success')
            return redirect(url_for('auth.change_password'))
        else:
            flash('Old password is incorrect.', 'danger')
    return render_template('auth/change_password.html', form=form)

# Route for viewing and editing user profile
@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Route for viewing and editing user profile.
    """
    user = User.query.get_or_404(current_user.id)
    form = EditProfileForm(obj=user)

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.major = form.major.data
        db.session.commit()

        # Update session data to reflect changes
        session['user_name'] = f"{user.first_name} {user.last_name}"
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('auth/profile.html', form=form)

# Route for accessing a secret page, available only to authenticated users
@auth.route('/secret')
@login_required
def secret():
    """
    Route for accessing a secret page, available only to authenticated users.
    """
    return 'Only authenticated users are allowed!'
