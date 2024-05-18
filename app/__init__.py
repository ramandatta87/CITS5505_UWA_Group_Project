from flask import Flask
from flask_login import LoginManager  # Import LoginManager for managing user sessions
from flask_mail import Mail  # Importing flask_email module
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for database management
from flask_migrate import Migrate  # Import Migrate for database migrations
from .config import Config  # Import the configuration settings
from flask_ckeditor import CKEditor  # Import CKEditor for rich text editing
from flask_session import Session  # Import Session for server-side session management

# Initialize extensions without attaching them to the app
db = SQLAlchemy()
session = Session()  # Initialize Flask-Session
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()  # Initialize LoginManager

def create_app(config_class=Config):
    """
    Create and configure an instance of the Flask application.
    """
    # Create the Flask application instance
    app = Flask(__name__)

    # Initialize CKEditor with the app
    ckeditor = CKEditor(app)

    # Apply configuration settings from the Config class
    app.config.from_object(config_class)

    # Initialize database and migration engine with the app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize Mail with the app
    mail.init_app(app)

    # Initialize LoginManager with the app
    login_manager.init_app(app)

    # Set the login view for LoginManager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please log in to access this page."  # Optional: Customize the login message

    # User loader callback to reload the user object from the user ID stored in the session
    @login_manager.user_loader
    def load_user(user_id):
        from app.model.models import User  # Import inside to avoid circular import issues
        return User.query.get(int(user_id))

    # Import and register blueprints for different parts of the application
    from app.controllers.auth_controller import auth
    from app.controllers.main_controller import main

    # Register 'auth' blueprint with URL prefix '/auth'
    app.register_blueprint(auth, url_prefix='/auth')

    # Register 'main' blueprint without URL prefix
    app.register_blueprint(main)
    
    return app
