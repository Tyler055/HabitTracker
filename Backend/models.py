from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

# Check database file path
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'habit_tracker.db')
print(f"Database file path: {db_path}")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
