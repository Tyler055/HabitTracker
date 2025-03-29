from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_pymongo import PyMongo

# Initialize the extensions
db = SQLAlchemy()
ma = Marshmallow()
mail = Mail()
mongo = PyMongo()
