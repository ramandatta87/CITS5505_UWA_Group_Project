from app import  db
from app.models.model import Posts

def test_register_page(test_client):
    response = test_client.get('/auth/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_register_user(test_client, init_database):
    response = test_client.post('/auth/register',
                                data=dict(
                                    first_name='New',
                                    last_name='User',
                                    uwa_id='87654321',
                                    email='newuser@example.com',
                                    major='New Major',
                                    password='password',
                                    confirm_password='password'
                                ),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Registration successful! You can now login." in response.data

def test_login_page(test_client):
    response = test_client.get('/auth/login')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_login_user(test_client, init_database):
    response = test_client.post('/auth/login',
                                data=dict(email='testuser@example.com', password='password'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Logout" in response.data

def test_logout_user(test_client):
    test_client.post('/auth/login',
                     data=dict(email='testuser@example.com', password='password'),
                     follow_redirects=True)
    response = test_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data

def test_profile_update(test_client, init_database, login_default_user):
    response = test_client.post('/auth/profile', data=dict(
        first_name='Updated',
        last_name='User',
        major='Updated Major'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Your profile has been updated.' in response.data

def test_add_post(test_client, init_database, login_default_user):
    response = test_client.post('/add_post', data=dict(
        title='Test Post',
        content='This is a test post.',
        tag='Test Tag',
        question_type='career',
        submit=True  # Indicating that the form should be submitted
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Blog Post Submitted Successfully' in response.data

def test_favorite_post(test_client, init_database, login_default_user):
    post = Posts(title='Favorite Test Post', content='This is a favorite test post.', tag_id=1, career_preparation=False, author_id=1, deleted=False, answered=False, is_draft=False)
    db.session.add(post)
    db.session.commit()

    response = test_client.post(f'/favorite_post/{post.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Post added to favorites' in response.data

    response = test_client.get('/my_favorites')
    assert response.status_code == 200
    assert b'Favorite Test Post' in response.data


def test_view_post(test_client, init_database, login_default_user):
    post = Posts(title='Test Post', content='This is a test post.', tag_id=1, career_preparation=False, author_id=1, deleted=False, answered=False, is_draft=False)
    db.session.add(post)
    db.session.commit()

    response = test_client.get(f'/post/{post.id}')
    assert response.status_code == 200
    assert b'Test Post' in response.data
    assert b'This is a test post.' in response.data

def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Adjust this according to your actual homepage content
