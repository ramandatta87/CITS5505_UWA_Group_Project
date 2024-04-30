
from flask import render_template, request, url_for, flash, redirect
from .forms import RegisterForm  # Importing the form Class
from .models import User, db

def init_routes(app):
    @app.route("/")
    @app.route("/index")
    @app.route("/home")
    def index():
        return render_template("index.html", login=False)

    @app.cli.command('db_create')
    def db_create():
        db.create_all()
        print("Database Created")

    @app.cli.command('db_drop')
    def db_drop():
        db.drop_all()
        print("Database Dropped")

        
    @app.route("/forum")
    def forum():
        return render_template("forum.html")

    @app.route("/register",methods=['GET', 'POST'])
    def register():
        form = RegisterForm(request.form)
        if request.method == 'POST' and form.validate():
            # Check if the email or UWA ID already exists
            existing_user = User.query.filter((User.email == form.email.data) | (User.uwa_id == form.uwa_id.data)).first()
            if existing_user is None:
                # Create a new user instance
                new_user = User(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    uwa_id=form.uwa_id.data,
                    email=form.email.data,
                    major=form.major.data
                )
                # Hash and set the password
                new_user.set_password(form.password.data)
                
                try:

                    # Add the new user to the database
                    db.session.add(new_user)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print("Failed to commit the transaction:", str(e))
                    flash("Failed to register the user.", "error")
                # Flash a success message
                flash('Registration successful! You can now login.', 'success')
                # Redirect to the login page or home page after registration
                return redirect(url_for('login'))
            else:
                # Flash an error message if the email or UWA ID already exists
                flash('Email or UWA ID already exists. Please use a different email or UWA ID.', 'error')

        # Render the register template with the form
        return render_template("register.html", form=form)

    @app.route("/login")
    def login():
        return render_template("login.html")