import pytest
from app import create_app, db
from backend.src.models import User, Habit  # Adjusted to reflect the correct relative module path
from werkzeug.security import generate_password_hash

# Test fixtures
@pytest.fixture
def app():
    """Set up the Flask app for testing with the testing config."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use in-memory DB for tests
        "WTF_CSRF_ENABLED": False  # Disable CSRF for easier testing
    })

    with app.app_context():
        db.create_all()  # Create tables for tests

    yield app  # Provide the app instance for tests

    with app.app_context():
        db.session.remove()
        db.drop_all()  # Clean up DB after each test

@pytest.fixture
def client(app):
    """Fixture to get the test client."""
    return app.test_client()

@pytest.fixture
def user(app):
    """Create a test user."""
    with app.app_context():
        hashed_password = generate_password_hash("password123")
        test_user = User(username="testuser", email="testuser@example.com", password=hashed_password)
        db.session.add(test_user)
        db.session.commit()
        return test_user

# Tests
def test_home(client):
    """Test the home route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Adjust based on your actual home page content

def test_user_registration(client):
    """Test user registration route."""
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpassword',
        'password2': 'newpassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Account created' in response.data  # Adjust based on your success message

    with db.session.no_autoflush:
        new_user = User.query.filter_by(username='newuser').first()
        assert new_user is not None
        assert new_user.email == 'newuser@example.com'

def test_user_login(client, user):
    """Test user login route."""
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Welcome' in response.data  # Adjust based on your actual success message

def test_user_login_invalid(client):
    """Test login with invalid credentials."""
    response = client.post('/auth/login', data={
        'username': 'wronguser',
        'password': 'wrongpassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid username or password' in response.data  # Adjust based on your actual error message

def test_habit_creation(client, user):
    """Test creating a habit."""
    client.post('/auth/login', data={'username': 'testuser', 'password': 'password123'}, follow_redirects=True)

    response = client.post('/habits/add', data={'name': 'Exercise'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Habit added' in response.data  # Adjust based on your actual success message

def test_habit_list(client, user):
    """Test viewing the list of habits."""
    client.post('/auth/login', data={'username': 'testuser', 'password': 'password123'}, follow_redirects=True)
    
    # Create a habit first
    client.post('/habits/add', data={'name': 'Exercise'}, follow_redirects=True)
    
    response = client.get('/habits', follow_redirects=True)
    assert response.status_code == 200
    assert b'Exercise' in response.data  # Adjust based on your actual habit list page content

def test_habit_deletion(client, user):
    """Test deleting a habit."""
    client.post('/auth/login', data={'username': 'testuser', 'password': 'password123'}, follow_redirects=True)

    # Create a habit first
    response = client.post('/habits/add', data={'name': 'Exercise'}, follow_redirects=True)
    assert response.status_code == 200

    # Now delete the habit
    with db.session.no_autoflush:
        habit = Habit.query.filter_by(name="Exercise").first()
        response = client.post(f'/habits/delete/{habit.id}', follow_redirects=True)
        assert response.status_code == 200
        assert b'Habit deleted' in response.data  # Verify success message

        # Ensure the habit is removed from the database
        habit = Habit.query.filter_by(name="Exercise").first()
        assert habit is None  # Habit should no longer exist

if __name__ == "__main__":
    pytest.main()
