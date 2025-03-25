from flask import Flask, render_template
from flask_login import LoginManager
from app import db
from routes import register_blueprints
import os

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

# Error handling for 404 and 500
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

if __name__ == "__main__":
    # Check if running in production mode, otherwise use debug mode
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(debug=False)
    else:
        app.run(debug=True)
