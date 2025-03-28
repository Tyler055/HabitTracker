from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


# -------------------- User Model --------------------
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Increased for full hash
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    habit_completions = db.relationship('HabitCompletion', backref='user', lazy=True, cascade="all, delete-orphan")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# -------------------- Habit Model --------------------
class Habit(db.Model):
    __tablename__ = 'habits'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    completions = db.relationship('HabitCompletion', backref='habit', lazy=True, cascade="all, delete-orphan")
    reminders = db.relationship('HabitReminder', backref='habit', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Habit {self.name}>'


# -------------------- Habit Completion Model --------------------
class HabitCompletion(db.Model):
    __tablename__ = 'habit_completions'

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    completed_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<HabitCompletion habit_id={self.habit_id} user_id={self.user_id} completed_at={self.completed_at}>'


# -------------------- Habit Reminder Model --------------------
class HabitReminder(db.Model):
    __tablename__ = 'habit_reminders'

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    reminder_time = db.Column(db.Time, nullable=False)
    reminder_message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    habit = db.relationship(
        'Habit',
        backref=db.backref('reminders', lazy=True, cascade='all, delete-orphan')
    )

    def __repr__(self):
        return f'<HabitReminder habit_id={self.habit_id} reminder_time={self.reminder_time}>'
