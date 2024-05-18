import os
import time

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = "Drmhze6EPcv0fN_81Bj-nA"
    PERMANENT_SESSION_LIFETIME = 1800  # Session lifetime in seconds (e.g., 1800 seconds = 30 minutes)
    SERVER_START_TOKEN = str(time.time())  # Generates a new token every time the server restarts
    
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "sqldb.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Session configuration
    SESSION_TYPE = 'sqlalchemy'  # Use SQLAlchemy for server-side session storage
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_SQLALCHEMY_TABLE = 'sessions'  # Table name for storing session data

    # Flask-Mail configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'cssedevconnect@gmail.com'  # Gmail email address
    MAIL_PASSWORD = 'urin uqte xesu euuh'  # Gmail password - Using Google App Generator
    MAIL_USE_SSL = False
    
    # Cookie settings
    SESSION_COOKIE_SECURE = True  # Ensure cookies are sent over SSL/TLS
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookies
    SESSION_COOKIE_SAMESITE = 'Lax'  # SameSite attribute for cookies

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False  # Turned off for testing
