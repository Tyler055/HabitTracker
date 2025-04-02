import pytest
from app.app import create_app
from app.models.models import db, Habit, User, HabitCompletion

# Test Configuration class
class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use an in-memory DB for testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True

@pytest.fixture
def app():
    app = create_app(config_class=TestingConfig)
    with app.app_context():  # Ensure the app context is available
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_db(app):
    # Set up the database with a test user and habit
    with app.app_context():
        db.create_all()

        # Create a test user
        user = User(username='test_user', password='test_password')
        db.session.add(user)

        # Create a test habit
        habit = Habit(name='Drink Water', frequency='daily', user_id=user.id)
        db.session.add(habit)
        db.session.commit()

    # Return the test user and habit
    return user, habit

@pytest.fixture(autouse=True)
def cleanup_db(app):
    # Ensure the database is cleaned up after each test
    with app.app_context():
        yield
        db.session.remove()
        db.drop_all()

# Test for creating habit completion
def test_create_habit_completion(client, init_db):
    user, habit = init_db

    # Create a completion for the habit
    response = client.post(f'/api/habits/{habit.id}/complete', json={'user_id': user.id})

    # Assert that the response status is 201 (Created)
    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"
    assert b"success" in response.data, f"Expected 'success' in the response, got: {response.data}"
    assert b"Habit marked as completed" in response.data, f"Expected 'Habit marked as completed' in the response, got: {response.data}"

    # Verify that the completion was added to the database
    completion = HabitCompletion.query.filter_by(habit_id=habit.id, user_id=user.id).first()
    assert completion is not None, "Completion not found in database"
    assert completion.user_id == user.id, f"Expected user_id {user.id}, got {completion.user_id}"
    assert completion.habit_id == habit.id, f"Expected habit_id {habit.id}, got {completion.habit_id}"
    assert completion.completed_at is not None, "completed_at is None"

# Test for getting user completions
def test_get_user_completions(client, init_db):
    user, habit = init_db

    # Create a completion for the habit
    client.post(f'/api/habits/{habit.id}/complete', json={'user_id': user.id})

    # Get all completions for the user
    response = client.get(f'/api/users/{user.id}/completions')

    # Assert that the response status is 200 (OK)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"

    # Check that the response contains the habit completion data
    data = response.get_json()
    assert len(data['data']) == 1, f"Expected 1 completion, got {len(data['data'])}"
    assert data['data'][0]['habit_id'] == habit.id, f"Expected habit_id {habit.id}, got {data['data'][0]['habit_id']}"
    assert data['data'][0]['completed_at'] is not None, "Expected completed_at to be present"

# Test for resetting user completions
def test_reset_user_completions(client, init_db):
    user, habit = init_db

    # Create a completion for the habit
    client.post(f'/api/habits/{habit.id}/complete', json={'user_id': user.id})

    # Reset completions for the user
    response = client.post(f'/api/users/{user.id}/completions/reset')

    # Assert that the response status is 200 (OK)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert b"All habit completions reset" in response.data, f"Expected 'All habit completions reset' in the response, got: {response.data}"

    # Verify that all completions are deleted
    completions = HabitCompletion.query.filter_by(user_id=user.id).all()
    assert len(completions) == 0, f"Expected 0 completions, got {len(completions)}"
