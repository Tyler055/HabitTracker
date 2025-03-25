import os
import time
import random
from werkzeug.utils import secure_filename
from flask import Blueprint, request, flash, redirect, url_for, send_from_directory, render_template
from werkzeug.datastructures import FileStorage

# Initialize Blueprint
files = Blueprint('files', __name__, url_prefix='/files')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'xls', 'xlsx', 'csv'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check if the file extension is allowed
def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to save the uploaded file to the server's filesystem
def save_file(file: FileStorage) -> str:
    """Save the file to the server."""
    if file and allowed_file(file.filename):
        # Secure the filename and construct the file path
        filename = secure_filename(file.filename)
        timestamp = int(time.time())  # Add timestamp to avoid filename conflicts
        unique_filename = f"{timestamp}_{random.randint(1000, 9999)}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        try:
            file.save(file_path)  # Save the file to the server
            return unique_filename
        except Exception as e:
            flash(f"Error saving file: {e}", 'danger')
            return None
    else:
        flash("Invalid file type. Only supported file types are: PNG, JPG, JPEG, GIF, TXT, PDF, DOCX.", 'danger')
        return None

# Function to get the full file path of an uploaded file
def get_file_path(filename: str) -> str:
    """Return the full path of the file."""
    return os.path.join(UPLOAD_FOLDER, filename)

# Function to delete the uploaded file from the server
def delete_file(filename: str) -> bool:
    """Delete the file from the server."""
    file_path = get_file_path(filename)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)  # Delete the file
            return True
        else:
            flash("File not found.", 'warning')
            return False
    except Exception as e:
        flash(f"Error deleting file: {e}", 'danger')
        return False

# Route to upload a file
@files.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        filename = save_file(file)  # Save the uploaded file
        if filename:
            flash(f'File {filename} uploaded successfully!', 'success')
            return redirect(url_for('files.upload_file'))  # Redirect to the same page
        else:
            return redirect(request.url)

    return render_template('upload/upload.html')

# Route to delete a file
@files.route('/delete/<filename>', methods=['GET', 'POST'])
def delete(filename):
    success = delete_file(filename)  # Call delete_file to remove the file
    if success:
        flash(f"File '{filename}' deleted successfully.", 'success')
    else:
        flash(f"Failed to delete file '{filename}'.", 'danger')
    return redirect(url_for('files.upload_file'))  # Redirect to the upload page

# Route to download a file
@files.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Handles file download."""
    file_path = get_file_path(filename)
    if not os.path.exists(file_path):
        flash(f"File '{filename}' does not exist.", 'danger')
        return redirect(url_for('files.upload_file'))
    
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except Exception as e:
        flash(f"File download failed: {str(e)}", 'danger')
        return redirect(url_for('files.upload_file'))  # Redirect to the upload page
