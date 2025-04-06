# app/utils/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)
mongo = PyMongo()
mail = Mail()
jwt = JWTManager()
login_manager = LoginManager()
