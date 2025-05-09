import os
from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

# ─── Load Environment Variables ─────────────────────────────
load_dotenv()

# ─── Flask App Configuration ───────────────────────────────
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'WebApp', 'templates')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'WebApp', 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = os.urandom(24)

# Enable auto-reload of templates for development
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configure session cookie settings
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=os.getenv('FLASK_ENV') == 'production',  # Ensure secure cookies in production
    SESSION_COOKIE_SAMESITE='Lax',
)

# ─── Email Configuration ───────────────────────────────────
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.example.com')  # Default to example
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))  # Default to 587
app.config['MAIL_USE_TLS'] = True  # TLS support
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Ensure MAIL_USERNAME is set in .env
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Ensure MAIL_PASSWORD is set in .env
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'your_email@example.com')

# Validate email configuration (ensure variables are set)
if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
    raise ValueError("MAIL_USERNAME and MAIL_PASSWORD must be set in environment variables.")

# Initialize Flask-Mail
mail = Mail(app)

# ─── Register Blueprints ─────────────────────────────────────
from auth import auth_bp
from views import views_bp
from api import api_bp

app.register_blueprint(auth_bp)
app.register_blueprint(views_bp)
app.register_blueprint(api_bp, url_prefix='/api')

# ─── Error Handling ─────────────────────────────────────────
@app.errorhandler(HTTPException)
def handle_exception(e):
    # Handle all exceptions (e.g., 404, 500, etc.) here
    return f"An error occurred: {e}", e.code

# ─── Run the App ───────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
