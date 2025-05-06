# app.py
import os
from flask import Flask
from dotenv import load_dotenv

# ─── Load Environment Variables ─────────────────────────────
load_dotenv()

# ─── Flask App Configuration ───────────────────────────────
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'WebApp', 'templates')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'WebApp', 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = os.urandom(24)

app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

# ─── Register Blueprints ─────────────────────────────────────
from auth import auth_bp
from views import views_bp
from api import api_bp

app.register_blueprint(auth_bp)
app.register_blueprint(views_bp)
app.register_blueprint(api_bp, url_prefix='/api')

# ─── Run the App ───────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
