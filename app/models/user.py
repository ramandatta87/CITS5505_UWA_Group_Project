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
    user_image = db.Column(db.String(200))  # Path to the image file
    is_disabled = db.Column(db.Boolean, default=False)  # Boolean to check if user is disabled
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of user creation
    role = db.Column(db.String(100))  # Role of the user

    #Method to securely set the user's password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to provide a string representation of the User object
    def __repr__(self):
        return f'<User {self.email}>'
