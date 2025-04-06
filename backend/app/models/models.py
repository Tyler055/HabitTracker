from datetime import datetime, time, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app.__init__ import db

# -------------------- Soft Delete Mixin --------------------
class SoftDeleteMixin:
    deleted_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def soft_delete(self):
        """Mark an instance as deleted without removing it from the DB."""
        self.deleted_at = datetime.now(timezone.utc)
        self.is_active = False

    def restore(self):
        """Restore a soft-deleted instance."""
        self.deleted_at = None
        self.is_active = True

    def is_active_method(self):
        """Check if the instance is active (not soft-deleted)."""
        return self.is_active and self.deleted_at is None


# -------------------- User Model --------------------
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    _password_hash = db.Column("password", db.String(255), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
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


# -------------------- Habit Model --------------------
class Habit(db.Model, SoftDeleteMixin):
    __tablename__ = 'habits'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    frequency = db.Column(db.String(20), default='daily')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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

    def __repr__(self):
        return f"<Habit {self.name}>"


# -------------------- Habit Completion Model --------------------
class HabitCompletion(db.Model, SoftDeleteMixin):
    __tablename__ = 'habit_completions'
    
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<HabitCompletion habit={self.habit_id} user={self.user_id}>"


# -------------------- Habit Reminder Model --------------------
class HabitReminder(db.Model, SoftDeleteMixin):
    __tablename__ = 'habit_reminders'
    
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reminder_time = db.Column(db.Time, nullable=False)
    reminder_message = db.Column(db.String(255), nullable=False)

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

    def __repr__(self):
        return f"<HabitAnalytics habit={self.habit_id} total={self.total_completions} streak={self.current_streak}>"

