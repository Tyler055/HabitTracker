from datetime import datetime, time, timezone
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Initialize SQLAlchemy
db = SQLAlchemy()

# -------------------- Soft Delete Mixin --------------------
class SoftDeleteMixin(db.Model):
    __abstract__ = True
    deleted_at = db.Column(db.DateTime, nullable=True)
    _is_active = db.Column("is_active", db.Boolean, default=True)

    def soft_delete(self):
        self.deleted_at = datetime.now(timezone.utc)
        self._is_active = False

    def restore(self):
        self.deleted_at = None
        self._is_active = True

    @hybrid_property
    def is_active(self):
        return self._is_active and self.deleted_at is None

# -------------------- User Model --------------------
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column("password_hash", db.String(200), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    habits = db.relationship('Habit', backref='user', lazy=True)
    completions = db.relationship('HabitCompletion', backref='user', lazy=True)
    reminders = db.relationship('HabitReminder', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
    from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    theme = db.Column(db.String(20), default='light')  # Add theme field

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# -------------------- Habit Frequency Enum --------------------
class FrequencyEnum(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

# -------------------- Habit Model --------------------
class Habit(SoftDeleteMixin):
    __tablename__ = 'habits'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    frequency = db.Column(db.Enum(FrequencyEnum, native_enum=False), default=FrequencyEnum.DAILY)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    completions = db.relationship('HabitCompletion', backref='habit', lazy=True, cascade="all, delete-orphan")
    reminders = db.relationship('HabitReminder', backref='habit', lazy=True, cascade="all, delete-orphan")
    analytics = db.relationship('HabitAnalytics', backref='habit', uselist=False, cascade="all, delete-orphan")

    def set_default_reminder(self):
        if not HabitReminder.query.filter_by(habit_id=self.id).first():
            reminder = HabitReminder(
                habit_id=self.id,
                user_id=self.user_id,
                reminder_time=time(9, 0),
                reminder_message=f"Reminder for {self.name}"
            )
            db.session.add(reminder)
            db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'frequency': self.frequency.value,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active
        }

    def __repr__(self):
        return f"<Habit {self.name}>"

# -------------------- Habit Completion Model --------------------
class HabitCompletion(SoftDeleteMixin):
    __tablename__ = 'habit_completions'

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    completed_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'habit_id': self.habit_id,
            'user_id': self.user_id,
            'completed_at': self.completed_at.isoformat()
        }

    def __repr__(self):
        return f"<HabitCompletion habit={self.habit_id} user={self.user_id}>"

# -------------------- Habit Reminder Model --------------------
class HabitReminder(SoftDeleteMixin):
    __tablename__ = 'habit_reminders'

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    reminder_time = db.Column(db.Time, nullable=False)
    reminder_message = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.reminder_time:
            self.reminder_time = time(9, 0)

    def to_dict(self):
        return {
            'id': self.id,
            'habit_id': self.habit_id,
            'user_id': self.user_id,
            'reminder_time': self.reminder_time.isoformat(),
            'reminder_message': self.reminder_message
        }

    def __repr__(self):
        return f"<HabitReminder '{self.reminder_message}' at {self.reminder_time}>"

# -------------------- Habit Analytics Model --------------------
class HabitAnalytics(db.Model):
    __tablename__ = 'habit_analytics'

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False, unique=True)
    total_completions = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_completed = db.Column(db.DateTime, nullable=True)

    def update_on_completion(self, completed_at):
        if self.last_completed and completed_at < self.last_completed:
            return

        self.total_completions += 1
        if self.last_completed:
            delta = (completed_at.date() - self.last_completed.date()).days
            if delta == 1:
                self.current_streak += 1
            elif delta > 1:
                self.current_streak = 1
        else:
            self.current_streak = 1

        self.longest_streak = max(self.longest_streak, self.current_streak)
        self.last_completed = completed_at

    def to_dict(self):
        return {
            'id': self.id,
            'habit_id': self.habit_id,
            'total_completions': self.total_completions,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'last_completed': self.last_completed.isoformat() if self.last_completed else None
        }

    def __repr__(self):
        return f"<HabitAnalytics habit={self.habit_id} total={self.total_completions} streak={self.current_streak}>"
