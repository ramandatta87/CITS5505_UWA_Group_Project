import pytest
from app import create_app, db
from app.models.model import User,  Tag  # Adjusted import path


from app.config import TestingConfig  # Import the TestingConfig class
from datetime import datetime
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='module')
def test_client():
    """
    Fixture for setting up the Flask test client.
    This client is used to make requests to the application during testing.

    Scope: module
    """
    flask_app = create_app(TestingConfig)
    
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
        yield testing_client
        with flask_app.app_context():
            db.drop_all()

@pytest.fixture(scope='module')
def init_database():
    """
    Fixture for initializing the database with test data.

    Scope: module
    """
    db.create_all()
    
    user = User(
        first_name='Test',
        last_name='User',
        uwa_id='12345678',
        email='testuser@example.com',
        major='Test Major',
        is_disabled=False,
        timestamp=datetime.utcnow(),
        role='user'
    )
    user.set_password('password')  # Assuming you have a method to set the password
    db.session.add(user)
    db.session.commit()             # Commit the user to the database

    yield db

    db.session.remove()             # Clean up after tests
    db.drop_all()                   # Drop all database tables

@pytest.fixture(scope='function')
def login_default_user(test_client):
    """
    Fixture for logging in a default test user before each test function.
    
    Scope: function
    """
    test_client.post('/auth/login', data=dict(
        email='testuser@example.com',
        password='password'
    ), follow_redirects=True)

    yield                           # This is where the testing happens

    test_client.get('/auth/logout', follow_redirects=True)