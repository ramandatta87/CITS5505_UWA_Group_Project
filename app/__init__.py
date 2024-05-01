from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from .config import Config 
from .models import db, User  # Import db here from models
from flask_migrate import Migrate


# Initialize the SQLAlchemy instance without passing the app
#db = SQLAlchemy()
migrate = Migrate()
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)  # Load configuration

    db.init_app(app)  # Link the SQLAlchemy instance to the Flask app

    migrate.init_app(app, db)

 
    # Importing models here ensures they're aware of the db instance
    from .models import User

    # Register routes
    from .routes import init_routes
    init_routes(app)  # Assuming routes are set up to accept an app instance

    # Optional: Create database tables within an app context
    with app.app_context():
        db.create_all()

    return app
