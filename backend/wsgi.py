from app import create_app

# Create the Flask app using the factory function
app = create_app()

if __name__ == "__main__":
    # This is for development, if you run this file directly (e.g., using python wsgi.py).
    app.run(debug=True)


