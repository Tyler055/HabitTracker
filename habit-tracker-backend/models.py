from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Habit {self.name}>"
