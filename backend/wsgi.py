from app.app import create_app
import os

# Create the app instance
app = create_app()

# Get the environment mode (defaults to 'production' if not set)
env_mode = os.getenv('ENV_MODE', 'production')

# Set the debug mode based on the environment
debug_mode = env_mode == 'development'
