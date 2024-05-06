from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

# Initialize SQLAlchemy and migration engine
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    # Create Flask app instance
    app = Flask(__name__)

    #Using Configuration Class
    app.config.from_object(config_class)

    # Initialize database and migration engine with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints for different parts of the application
    from app.controllers.auth_controller import auth
    from app.controllers.main_controller import main

    # Register 'auth' blueprint with URL prefix '/auth'
    app.register_blueprint(auth, url_prefix='/auth')

    # Register 'main' blueprint without URL prefix
    app.register_blueprint(main)

    return app
