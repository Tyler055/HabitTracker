import os
from flask import Blueprint, request, flash, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app import db
from models import File  # Assuming you have a `File` model for tracking uploaded files

# Set allowed file extensions and max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'csv'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 MB in bytes

# Define the uploads directory
UPLOAD_FOLDER = 'app/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create a Blueprint for file-related routes
files = Blueprint("files", __name__)

# Check if a file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for file uploading
@files.route("/upload", methods=["POST"])
@login_required
def upload_file():
    """Handle file uploads."""
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)

    file = request.files['file']

    # If the user does not select a file or file is empty
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)

    # Check for allowed file extension and size
    if file and allowed_file(file.filename):
        # Ensure the file is safe to use
        filename = secure_filename(file.filename)
        
        # Check if file size is within the allowed limit
        if len(file.read()) > MAX_FILE_SIZE:
            flash('File exceeds maximum allowed size of 16MB', 'danger')
            return redirect(request.url)
        
        # Reset the file pointer to the beginning after checking size
        file.seek(0)

        # Save the file to the server
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Optionally save file information to the database (e.g., name, path, user)
        new_file = File(filename=filename, filepath=file_path, user_id=current_user.id)
        db.session.add(new_file)
        db.session.commit()

        flash('File uploaded successfully!', 'success')
        return redirect(url_for('files.view_files'))
    
    flash('File type not allowed or invalid', 'danger')
    return redirect(request.url)

# Route to view uploaded files (for example)
@files.route("/view")
@login_required
def view_files():
    """Display all uploaded files for the logged-in user."""
    user_files = File.query.filter_by(user_id=current_user.id).all()
    return render_template("files.html", files=user_files)
