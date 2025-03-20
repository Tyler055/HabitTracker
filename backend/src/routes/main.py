from flask import Flask
from flask_login import LoginManager
from app import db
from routes import register_blueprints

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object('config.Config')  # Your config class to load settings

# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Redirect unauthenticated users to the login page

# Register blueprints
register_blueprints(app)

# Initialize the database
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
