from datetime import datetime, time, timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# -------------------- Soft Delete Mixin --------------------
class SoftDeleteMixin:
    deleted_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def soft_delete(self):
        """Mark an instance as deleted without removing it from the DB."""
        self.deleted_at = datetime.utcnow()
        self.is_active = False

    def restore(self):
        """Restore a soft-deleted instance."""
        self.deleted_at = None
        self.is_active = True

# -------------------- User Model --------------------
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    _password_hash = db.Column("password", db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    habits = db.relationship('Habit', backref='user', lazy=True)
    completions = db.relationship('HabitCompletion', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password_hash, password)

# -------------------- Habit Model --------------------
class Habit(db.Model, SoftDeleteMixin):
    __tablename__ = 'habits'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    frequency = db.Column(db.String(20), default='daily')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    completions = db.relationship('HabitCompletion', backref='habit', lazy=True, cascade="all, delete-orphan")
    reminders = db.relationship('HabitReminder', backref='habit', lazy=True, cascade="all, delete-orphan")
    analytics = db.relationship('HabitAnalytics', backref='habit', uselist=False, cascade="all, delete-orphan")

    def set_default_reminder(self):
        if not HabitReminder.query.filter_by(habit_id=self.id).first():
            reminder = HabitReminder(habit_id=self.id, reminder_time=time(9, 0), reminder_message=f"Reminder for {self.name}")
            db.session.add(reminder)
            db.session.commit()

# -------------------- Habit Completion Model --------------------
class HabitCompletion(db.Model, SoftDeleteMixin):
    __tablename__ = 'habit_completions'
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    completed_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# -------------------- Habit Reminder Model --------------------
class HabitReminder(db.Model, SoftDeleteMixin):
    __tablename__ = 'habit_reminders'
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    reminder_time = db.Column(db.Time, nullable=False)
    reminder_message = db.Column(db.String(255), nullable=False)

# -------------------- Habit Analytics Model --------------------
class HabitAnalytics(db.Model):
    __tablename__ = 'habit_analytics'
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False, unique=True)
    total_completions = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_completed = db.Column(db.DateTime, nullable=True)
