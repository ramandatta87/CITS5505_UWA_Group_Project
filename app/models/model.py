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

# Tag Model for Tagging Category in Posting 
class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Tag {self.tag}>'
    
class Posts(db.Model):
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)
    answered = db.Column(db.Boolean, default=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    career_preparation = db.Column(db.Boolean, default=False)
    is_draft = db.Column(db.Boolean, default=False)  # New column to indicate if the post is a draft

    author = db.relationship('User', backref=db.backref('posts', lazy=True))
    tag = db.relationship('Tag', backref=db.backref('posts', lazy=True))
    
    def __repr__(self):
        return f'<Posts {self.title}>'

    
# Reply Model
class Reply(db.Model):
    __tablename__ = "replies"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    answered_accepted = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    post = db.relationship('Posts', backref=db.backref('replies', lazy=True))
    author = db.relationship('User', backref=db.backref('replies', lazy=True))

    def __repr__(self):
        return f'<Reply {self.id}>'
    
# Favourite Post Model

class FavoritePost(db.Model):
    __tablename__ = "favorite_posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('favorites', lazy=True))
    post = db.relationship('Posts', backref=db.backref('favorited_by', lazy=True))
