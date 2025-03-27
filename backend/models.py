from flask_sqlalchemy import SQLAlchemy

# Initialize the database object
db = SQLAlchemy()

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Name of the habit
    completed = db.Column(db.Boolean, default=False)  # Whether the habit is completed or not

    def __repr__(self):
        return f"<Habit {self.name}>"
