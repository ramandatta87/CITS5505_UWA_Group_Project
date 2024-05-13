# Import necessary modules and functions(for password hashing and salting)
from flask_login import UserMixin
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    uwa_id = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    major = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    user_image = db.Column(db.String(200))
    is_disabled = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(100))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

    @property
    def is_active(self):
        return not self.is_disabled

class Posts(db.Model):
    __tablename__ = "Posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)
    answered = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Posts {self.title}>'
