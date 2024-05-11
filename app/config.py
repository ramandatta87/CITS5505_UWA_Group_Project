import os
import time

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = "Drmhze6EPcv0fN_81Bj-nA"
    PERMANENT_SESSION_LIFETIME = 1800  # Session lifetime in seconds (e.g., 1800 seconds = 30 minutes)
    SERVER_START_TOKEN = str(time.time())  # Generates a new token every time the server restarts
    
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "sqldb.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True  # Ensure cookies are sent over SSL/TLS
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookies
    SESSION_COOKIE_SAMESITE = 'Lax'  # Strict or Lax to pr

    # Flask-Mail configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'cssedevconnect@gmail.com'  # Gmail email address
    MAIL_PASSWORD = 'urin uqte xesu euuh'  # Gmail password - Using Google App Generator
    MAIL_USE_SSL = False
    