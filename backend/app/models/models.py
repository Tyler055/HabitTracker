from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Habit Model
class Habit(db.Model):
    __tablename__ = 'habits'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each habit
    name = db.Column(db.String(100), nullable=False)  # Habit name (non-nullable)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Timestamp for habit creation
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # Timestamp for habit updates

    def __repr__(self):
        return f'<Habit {self.name}>'

# Optional: User Model (if you need user authentication/management for your app)
class User(db.Model):
    __tablename__ = 'users'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    username = db.Column(db.String(100), unique=True, nullable=False)  # Username (unique and non-nullable)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email (unique and non-nullable)
    password = db.Column(db.String(100), nullable=False)  # Hashed password (non-nullable)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Timestamp for account creation
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # Timestamp for updates

    def __repr__(self):
        return f'<User {self.username}>'

# Optional: A model for habit tracking (if you want to track when habits are completed)
class HabitCompletion(db.Model):
    __tablename__ = 'habit_completions'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each habit completion record
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)  # Link to the Habit model
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Link to the User model
    completed_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Timestamp for when the habit was completed

    habit = db.relationship('Habit', backref=db.backref('completions', lazy=True))  # Relationship with Habit model
    user = db.relationship('User', backref=db.backref('habit_completions', lazy=True))  # Relationship with User model

    def __repr__(self):
        return f'<HabitCompletion habit_id={self.habit_id} user_id={self.user_id} completed_at={self.completed_at}>'

# Optional: A model for habit reminders (if you want to add reminders for habits)
class HabitReminder(db.Model):
    __tablename__ = 'habit_reminders'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each reminder
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)  # Link to the Habit model
    reminder_time = db.Column(db.Time, nullable=False)  # Time for the reminder
    reminder_message = db.Column(db.String(255), nullable=False)  # Message for the reminder
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Timestamp for when the reminder was created

    habit = db.relationship('Habit', backref=db.backref('reminders', lazy=True))  # Relationship with Habit model

    def __repr__(self):
        return f'<HabitReminder habit_id={self.habit_id} reminder_time={self.reminder_time}>'

