import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env
load_dotenv()

# Get environment mode and port
env_mode = os.getenv('APP_MODE', 'development')  # Corrected the typo here
debug_mode = env_mode == 'development'
port = int(os.getenv('PORT', 5000))

# Create app
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
