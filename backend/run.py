from app import create_app

# Create an instance of the Flask application
app = create_app()

# Run the app
if __name__ == "__main__":
    app.run(debug=True)  # Set debug to True for local development
