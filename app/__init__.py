# app/__init__.py
from flask import Flask
from .views.auth_views import auth_bp

def create_app():
    app = Flask(__name__)
    
    # Configure app
    app.config.from_object('config.Config')  # Make sure to set your config here

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
