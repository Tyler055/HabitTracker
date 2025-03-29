import os
from dotenv import load_dotenv
load_dotenv()  # Update the path if your .env is in a different location


def check_env_vars():
    # Get the current APP_MODE to determine which environment is active
    app_mode = os.getenv("APP_MODE")
    
    if not app_mode:
        print("Error: APP_MODE is not set.")
        return
    
    print(f"App Mode: {app_mode.capitalize()}")
    print("-" * 40)
    
    # Check and print the environment variables based on the app mode
    if app_mode == "test":
        print(f"Testing Database URI: {os.getenv('MYSQL_TEST_URI')}")
        print(f"Testing MongoDB URI: {os.getenv('MONGO_TEST_URI')}")
        print(f"Testing Database URL: {os.getenv('DATABASE_URL')}")
    elif app_mode == "development":
        print(f"Development MySQL URI: {os.getenv('MYSQL_DB_URI')}")
        print(f"Development MongoDB URI: {os.getenv('MONGO_DB_URI')}")
        print(f"Development Database URL: {os.getenv('DATABASE_URL')}")
    elif app_mode == "production":
        print(f"Production MySQL URI: {os.getenv('MYSQL_PROD_URI')}")
        print(f"Production MongoDB URI: {os.getenv('MONGO_PROD_URI')}")
        print(f"Production Redis URL: {os.getenv('REDIS_URL')}")
    else:
        print("Error: Invalid APP_MODE value.")
        return
    
    # Print additional environment settings (common across all modes)
    print("-" * 40)
    print(f"JWT Secret: {os.getenv('JWT_SECRET')}")
    print(f"Mail Server: {os.getenv('MAIL_SERVER')}")
    print(f"Upload Folder: {os.getenv('UPLOAD_FOLDER')}")
    print(f"Cache Type: {os.getenv('CACHE_TYPE')}")
    print(f"Port: {os.getenv('PORT')}")
    print(f"App Name: {os.getenv('APP_NAME')}")

if __name__ == "__main__":
    check_env_vars()
