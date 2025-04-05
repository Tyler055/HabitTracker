import os
from app.app import create_app

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Get environment mode from .env, default to 'development'
env_mode = os.getenv('FLASK_ENV', 'development')

# Create the Flask app based on the environment mode
app = create_app(env_mode)

if __name__ == "__main__":
    # Set debug mode based on environment
    debug_mode = env_mode == 'development'
    
    # Get port from environment variables or default to 5000
    port = int(os.getenv('PORT', 5000))
    
    # Run the app on the specified port and with the appropriate debug mode
    app.run(port=port, debug=debug_mode)
