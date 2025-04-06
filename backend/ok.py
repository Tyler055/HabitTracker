import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from config import DevelopmentConfig, TestingConfig, ProductionConfig

# Choose config based on APP_MODE
app_mode = os.getenv("APP_MODE", "development")  # Default to development if not set
if app_mode == "development":
    ActiveConfig = DevelopmentConfig
elif app_mode == "production":
    ActiveConfig = ProductionConfig
else:
    ActiveConfig = TestingConfig

# Init Flask app and config
app = Flask(__name__)
app.config.from_object(ActiveConfig)

# Test if environment variables are loaded correctly
print("MONGO_TEST_URI:", os.getenv("MONGO_TEST_URI"))
print("MYSQL_TEST_URI:", os.getenv("MYSQL_TEST_URI"))
print("MYSQL_DB_URI:", os.getenv("MYSQL_DB_URI"))
print("MONGO_DB_URI:", os.getenv("MONGO_DB_URI"))
print("SECRET_KEY:", os.getenv("SECRET_KEY"))
# Print the configuration settings instead of setting them
print('SQLALCHEMY_DATABASE_URI:', os.getenv("DATABASE_DB_URL") or ActiveConfig.SQLALCHEMY_DATABASE_URI)
print('SQLALCHEMY_TRACK_MODIFICATIONS:', False)  # Printing the setting, not assigning
print('MONGO_URI:', os.getenv("MONGO_DB_URI") or ActiveConfig.MONGO_URI)
print('JWT_SECRET_KEY:', os.getenv("JWT_SECRET_KEY", "super-secret-key"))
print('FRONTEND_URL:', os.getenv("FRONTEND_URL", "http://localhost:3000"))

# SQLAlchemy init
db = SQLAlchemy(app)

# Ensure Mongo URI is set correctly in app.config
mongo_uri = os.getenv("MONGO_DB_URI", "mongodb://localhost:27017/habit_tracker")  # Default to local MongoDB URI if not set
app.config["MONGO_URI"] = mongo_uri
mongo = PyMongo(app)

# Test SQLAlchemy connection
try:
    with app.app_context():
        db.create_all()  # This creates all tables based on models defined
        print("✅ SQLAlchemy connected successfully!")
except Exception as e:
    print(f"❌ SQLAlchemy error: {e}")

# Test MongoDB connection
try:
    mongo.db.list_collection_names()  # Test list of collections
    print("✅ MongoDB connected successfully!")
except Exception as e:
    print(f"❌ MongoDB error: {e}")
