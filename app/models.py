from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float

db = SQLAlchemy()

class User(db.Model):
    __tablename__= "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    uwa_id = db.Column(db.String(100), unique=True, nullable=False)  # UWA ID should be unique
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email should be unique
    major = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User {}>'.format(self.email)


    
