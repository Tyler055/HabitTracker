from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()

def init_extensions(app):
    if not app or not app.config:
        raise ValueError("Flask app is not initialized correctly")
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # Redirect to the login page if not logged in
    login_manager.login_message = "Please log in to access this page."

    mail.init_app(app)
    csrf.init_app(app, exempt=["api/*"])  # Example: Exempt API routes from CSRF protection
