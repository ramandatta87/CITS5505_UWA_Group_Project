# Import necessary modules and functions(for password hashing and salting)
from app import db
from werkzeug.security import generate_password_hash

#Defining the User Model Class

class User(db.Model):
    #Table Name
    __tablename__ = "users"

    #Defining the columns
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    uwa_id = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    major = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    #Method to securely set the user's password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to provide a string representation of the User object
    def __repr__(self):
        return f'<User {self.email}>'
