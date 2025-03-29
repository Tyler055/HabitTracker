from datetime import datetime, time, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Query
from app.utils.extensions import db

# -------------------- Soft Delete Base Query --------------------
class SoftDeleteQuery(Query):
    def __new__(cls, *args, **kwargs):
        obj = super(SoftDeleteQuery, cls).__new__(cls)
        return obj

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._with_deleted = False

    def with_deleted(self):
        self._with_deleted = True
        return self

    def get(self, ident):
        if self._with_deleted:
            return super().get(ident)
        return self.filter_by(id=ident, deleted_at=None).first()

    def __iter__(self):
        if not self._with_deleted:
            self = self.filter(self._only_not_deleted())
        return super().__iter__()

    def _only_not_deleted(self):
        if hasattr(self._entities[0].entity_zero.class_, 'deleted_at'):
            return self._entities[0].entity_zero.class_.deleted_at.is_(None)
        return True

# -------------------- User Model --------------------
class User(db.Model):
    __tablename__ = 'users'
    query_class = SoftDeleteQuery

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    habits = db.relationship('Habit', backref='user', lazy=True, cascade="all, delete-orphan")
    habit_completions = db.relationship('HabitCompletion', backref='user', lazy=True, cascade="all, delete-orphan")

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

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
    query_class = SoftDeleteQuery

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    completed = db.Column(db.Boolean, default=False)
    frequency = db.Column(db.String(20), default='daily')  # daily / weekly
    is_active = db.Column(db.Boolean, default=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    completions = db.relationship('HabitCompletion', backref='habit', lazy=True, cascade="all, delete-orphan")
    reminders = db.relationship('HabitReminder', backref='habit', lazy=True, cascade="all, delete-orphan")
    analytics = db.relationship('HabitAnalytics', backref='habit', uselist=False, cascade="all, delete-orphan")

    def set_default_reminder(self):
        default_time = time(9, 0)
        message = f"Reminder to complete your {self.frequency} habit: {self.name}"
        reminder = HabitReminder(habit_id=self.id, reminder_time=default_time, reminder_message=message)
        db.session.add(reminder)
        db.session.commit()

    def __repr__(self):
        return f'<Habit {self.name}>'

# -------------------- Habit Completion Model --------------------
class HabitCompletion(db.Model):
    __tablename__ = 'habit_completions'
    query_class = SoftDeleteQuery

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    completed_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    is_active = db.Column(db.Boolean, default=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<HabitCompletion habit_id={self.habit_id} user_id={self.user_id} completed_at={self.completed_at}>'

# -------------------- Habit Reminder Model --------------------
class HabitReminder(db.Model):
    __tablename__ = 'habit_reminders'
    query_class = SoftDeleteQuery

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    reminder_time = db.Column(db.Time, nullable=False)
    reminder_message = db.Column(db.String(255), nullable=False)

    is_active = db.Column(db.Boolean, default=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<HabitReminder habit_id={self.habit_id} reminder_time={self.reminder_time}>'

# -------------------- Habit Analytics Model --------------------
class HabitAnalytics(db.Model):
    __tablename__ = 'habit_analytics'

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False, unique=True)
    total_completions = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_completed = db.Column(db.DateTime, nullable=True)

    def update_on_completion(self, completion_time=None):
        now = completion_time or datetime.utcnow()
        if self.last_completed:
            delta = now.date() - self.last_completed.date()
            if delta == timedelta(days=1):
                self.current_streak += 1
            elif delta.days == 0:
                pass  # Same day
            else:
                self.current_streak = 1
        else:
            self.current_streak = 1

        self.total_completions += 1
        self.longest_streak = max(self.longest_streak, self.current_streak)
        self.last_completed = now

    def __repr__(self):
        return f'<HabitAnalytics habit_id={self.habit_id} total_completions={self.total_completions}>'
