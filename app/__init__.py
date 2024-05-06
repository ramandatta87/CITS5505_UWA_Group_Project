from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.controllers.auth_controller import auth
    from app.controllers.main_controller import main
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main)

    return app
