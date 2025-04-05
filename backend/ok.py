import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Test if environment variables are loaded correctly
print("MONGO_TEST_URI:", os.getenv("MONGO_TEST_URI"))
print("MYSQL_TEST_URI:", os.getenv("MYSQL_TEST_URI"))
print("DATABASE_URL:", os.getenv("DATABASE_URL"))
print("SECRET_KEY:", os.getenv("SECRET_KEY"))
