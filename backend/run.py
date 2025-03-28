from app import create_app
import os

# Create an instance of the Flask application
app = create_app()

# Run the app

debug_mode = os.getenv('FLASK_DEBUG', 'False') == 'True'
app.run(debug=debug_mode)
