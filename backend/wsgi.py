from app import create_app

# Create an instance of the Flask application
app = create_app()

# The `app` object will be used by the WSGI server (e.g., Gunicorn, uWSGI)
