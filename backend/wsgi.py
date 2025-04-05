from app import create_app
import os

# Create the app using the factory
app = create_app()

# Determine the environment mode
env_mode = os.getenv('ENV_MODE', 'production')
debug_mode = env_mode == 'development'

# Set the app's debug mode based on the environment
app.config['DEBUG'] = debug_mode

# Ensure the app is created before accessing its config
# Checking if APP_MODE exists in the config
app_mode = app.config.get('APP_MODE', 'Not defined in config')
print(f"Active config: {app_mode}")
print(f"Debug mode: {app.config['DEBUG']}")

# Run the app with the appropriate debug setting
if __name__ == "__main__":
    app.run(debug=debug_mode)
