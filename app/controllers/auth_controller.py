from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from app.models.user import User
from app.forms import RegisterForm, LoginForm, ForgetPasswordForm, ChangePasswordForm, EditProfileForm
from app import db, mail
from flask_mail import  Message


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
                major=form.major.data,
                is_disabled=False,
                timestamp=datetime.utcnow(),
                role='user'
            )
            new_user.set_password(form.password.data)
            try:
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

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['logged_in'] = True
            session['user_name'] = f"{user.first_name} {user.last_name}"
            session['user_id'] = user.id
            session['server_start_token'] = current_app.config['SERVER_START_TOKEN']
            return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@auth.before_app_request
def before_request():
    if 'server_start_token' in session:
        if session['server_start_token'] != current_app.config['SERVER_START_TOKEN']:
            session.clear()
            flash('Session has expired, please log in again.', 'info')
            return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        # Fetch the user based on UWA ID and Email for extra verification
        user = User.query.filter_by(uwa_id=form.uwa_id.data, email=form.email.data).first()
        if user and user.first_name == form.first_name.data:
            # Update the user's password
            user.password_hash = generate_password_hash(form.new_password.data)
            db.session.commit()
            # Send a confirmation email
            send_password_change_email(user)
            flash('Your password has been updated. Please check your email for confirmation.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('forgetpassword.html', form=form)

def send_password_change_email(user):
    msg = Message('Password Change Confirmation', sender='cssedevconnect@gmail.com', recipients=[user.email])
    msg.body = f'''Hello {user.first_name},

This is a confirmation that the password for your account {user.email} has just been changed.

If you did not make this change, please contact support immediately.

Best regards,
CSSE DevConnect
'''
    mail.send(msg)



@auth.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if not session.get('logged_in'):
        flash("Please log in to access this page.", "info")
        return redirect(url_for('auth.login'))
    
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user = User.query.get(session['user_id'])  # Ensure you have user_id in session

        if not check_password_hash(current_user.password_hash, form.old_password.data):
            flash('Invalid old password.', 'error')
            return render_template('change_password.html', form=form)

        current_user.password_hash = generate_password_hash(form.new_password.data)
        db.session.commit()
        
        session.clear()  # Clear the session to log out the user
        flash('Your password has been updated! Please log in again.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('change_password.html', form=form)
 

@auth.route('/profile', methods=['GET', 'POST'])
def profile():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please log in to view this page', 'info')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])  # Fetch the user based on session user_id
    form = EditProfileForm(obj=user)  # Pre-fill form with existing user details
    
    if request.method == 'POST' and form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        
        user.major = form.major.data
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('auth.profile'))  # Redirect to the profile page to see updated info
    
    return render_template('profile.html', form=form)

@auth.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'