import os
from app.app import create_app

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Get the environment mode from the .env file, defaulting to 'development'
env_mode = os.getenv('APP_MOD', 'development')

# Create the Flask app based on the environment mode
app = create_app(env_mode)

if __name__ == "__main__":
    # Set debug mode based on environment
    debug_mode = env_mode == 'development'
    
    # Get the port from environment variables or default to 5000
    port = int(os.getenv('PORT', 5000))
    
    # Run the app with the specified host, port, and debug mode
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
