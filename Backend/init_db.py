from flask import Flask
from dataservice import init_db

# Create a minimal Flask app
app = Flask(__name__)

with app.app_context():
    init_db()
    print("✅ Database initialized successfully.")
