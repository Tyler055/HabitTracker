from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from app.config import config  # Assuming you have separate config files
from app.extensions import db  # Import db from extensions.py
from .routes.habit_routes import habit_bp  # Import the habit blueprint

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configuration based on environment
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])  # Select config based on environment

# Set the database URI dynamically from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "mysql://root:password@localhost/habit-tracker")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To avoid overhead in modification tracking

# Initialize db with app
db.init_app(app)

# Initialize Migrate
migrate = Migrate(app, db)

# Register Blueprints (import habit_bp here)
app.register_blueprint(habit_bp)

# Home route
@app.route('/')
def home():
    return "Welcome to the Habit Tracker API!"

# Run the application
if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 5000)), debug=os.getenv("DEBUG", "True") == "True")
