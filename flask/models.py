import os
from datetime import datetime, timedelta, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model, UserMixin):
    """User model to store user information."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    theme = db.Column(db.String(20), default='dark')

    # One-to-many relationship with habits
    habits = db.relationship('Habit', backref='owner', lazy=True, cascade="all, delete-orphan")
    activity_logs = db.relationship('ActivityLog', backref='user', lazy=True)

    def set_password(self, password: str):
        """Hash and set the password for the user."""
        self.password_hash = generate_password_hash(password, method='sha256')

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the hashed password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class Habit(db.Model):
    """Habit model to track user habits and streaks."""
    __tablename__ = "habits"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Use UTC now instead of timezone.utc
    last_completed = db.Column(db.DateTime, nullable=True)
    streak = db.Column(db.Integer, default=0)

    def update_streak(self):
        """Update habit streak based on last completion date."""
        today = datetime.utcnow().date()
        
        if self.last_completed:
            last_date = self.last_completed.date()
            if last_date == today - timedelta(days=1):
                self.streak += 1
            elif last_date < today - timedelta(days=1):
                self.streak = 0  # Reset streak if more than one day is missed
        else:
            self.streak = 1
        
        self.last_completed = datetime.utcnow()  # Update with current UTC time

    def __repr__(self):
        return f"<Habit {self.name}, Streak: {self.streak}>"

class ActivityLog(db.Model):
    """Logs user activities for tracking purposes."""
    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Use UTC now

    log_type = db.Column(db.String(50), nullable=False, default="generic")  # Add log type

    def __repr__(self):
        return f"<ActivityLog {self.activity} at {self.timestamp}>"

class Message(db.Model):
    """Stores messages, supporting various message types."""
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Use UTC now
    message_type = db.Column(db.String(50), default="text")  # Message type can be "text", "image", etc.
    message_status = db.Column(db.String(20), default="unread")  # Add message status: "unread" or "read"
    is_response = db.Column(db.Boolean, default=False)  # Flag if message is AI response
    parent_message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=True)  # For threaded messages
    parent_message = db.relationship('Message', backref=db.backref('responses', remote_side=[id]))  # Parent-child relationship for threads

    def __repr__(self):
        return f"<Message {self.id}: {self.content[:50]}>"

class NeuralNetwork(db.Model):
    """Neural Network model to store AI-related data."""
    __tablename__ = "neural_network_data"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=False)  # AI-related data, could be JSON or raw text

    def __repr__(self):
        return f"<NeuralNetwork Data {self.id}>"
