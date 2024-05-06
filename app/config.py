import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = "Drmhze6EPcv0fN_81Bj-nA"
    
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "sqldb.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'cssedevconnect@gmail.com'  # Gmail email address
    MAIL_PASSWORD = 'urin uqte xesu euuh'  # Gmail password - Using Google App Generator
    MAIL_USE_SSL = False
    