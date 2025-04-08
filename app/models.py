from datetime import datetime, timedelta, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import re

# Initialize SQLAlchemy
db = SQLAlchemy()

def current_time():
    return datetime.now(timezone.utc)  # Timezone-aware UTC time

def is_password_valid(password: str) -> bool:
    """Check if the password meets complexity requirements."""
    return len(password) >= 8 and bool(re.search(r'[A-Za-z]', password)) and bool(re.search(r'\d', password))

class User(db.Model, UserMixin):
    """User model to store user information."""
    __tablename__ = "users"
    __table_args__ = (db.Index('ix_user_username', 'username'),)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    theme = db.Column(db.String(20), default='dark')

    habits = db.relationship('Habit', backref='owner', lazy=True, cascade="all, delete-orphan")
    activity_logs = db.relationship('ActivityLog', backref='user', lazy=True, cascade="all, delete-orphan")
    messages = db.relationship('Message', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str):
        """Hash and set the password for the user."""
        if not is_password_valid(password):
            raise ValueError("Password must be at least 8 characters long and contain both letters and numbers.")
        self.password_hash = generate_password_hash(password, method='sha256')

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the hashed password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

# Remaining models (Habit, ActivityLog, Message, NeuralNetwork) with similar timezone and cascading adjustments
