import pytest
from app.app import create_app
from app.models.models import db, Habit, User, HabitCompletion
from datetime import datetime

# Test Configuration class
@pytest.fixture
def app():
    app = create_app(config_class='TestingConfig')  # Use the testing config
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_db():
    # Set up the database with a test user and habit
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
def cleanup_db():
    # Ensure the database is cleaned up after each test
    yield
    db.session.remove()
    db.drop_all()

# Test for creating habit completion
def test_create_habit_completion(client, init_db):
    user, habit = init_db

    # Create a completion for the habit
    response = client.post(f'/api/habits/{habit.id}/complete', json={'user_id': user.id})

    # Assert that the response status is 201 (Created)
    assert response.status_code == 201
    assert b"success" in response.data
    assert b"Habit marked as completed" in response.data

    # Verify that the completion was added to the database
    completion = HabitCompletion.query.filter_by(habit_id=habit.id, user_id=user.id).first()
    assert completion is not None
    assert completion.user_id == user.id
    assert completion.habit_id == habit.id
    assert completion.completed_at is not None

# Test for getting user completions
def test_get_user_completions(client, init_db):
    user, habit = init_db

    # Create a completion for the habit
    client.post(f'/api/habits/{habit.id}/complete', json={'user_id': user.id})

    # Get all completions for the user
    response = client.get(f'/api/users/{user.id}/completions')

    # Assert that the response status is 200 (OK)
    assert response.status_code == 200

    # Check that the response contains the habit completion data
    data = response.get_json()
    assert len(data['data']) == 1
    assert data['data'][0]['habit_id'] == habit.id
    assert data['data'][0]['completed_at'] is not None

# Test for resetting user completions
def test_reset_user_completions(client, init_db):
    user, habit = init_db

    # Create a completion for the habit
    client.post(f'/api/habits/{habit.id}/complete', json={'user_id': user.id})

    # Reset completions for the user
    response = client.post(f'/api/users/{user.id}/completions/reset')

    # Assert that the response status is 200 (OK)
    assert response.status_code == 200
    assert b"All habit completions reset" in response.data

    # Verify that all completions are deleted
    completions = HabitCompletion.query.filter_by(user_id=user.id).all()
    assert len(completions) == 0
