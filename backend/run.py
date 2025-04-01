import os
from app.app import create_app

# Get environment mode from .env, default to development
env_mode = os.getenv('FLASK_ENV', 'development')

app = create_app(env_mode)

if __name__ == "__main__":
    debug_mode = env_mode == 'development'
    port = int(os.getenv('PORT', 5000))
    app.run(port=port, debug=debug_mode)
