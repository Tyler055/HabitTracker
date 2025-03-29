# run.py
import os
from app import create_app

# Get environment mode from .env, default to 'development'
env_mode = os.getenv('APP_MODE', 'development')

# Create the app with the appropriate environment configuration
app = create_app(env_mode)

if __name__ == "__main__":
    # Set debug mode based on the environment
    debug_mode = env_mode == 'development'
    
    # Get the port from environment variables, default to 5000
    port = int(os.getenv('PORT', 5000))
    
    # Run the app
    app.run(port=port, debug=debug_mode)
