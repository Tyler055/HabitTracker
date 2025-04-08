from flask import Blueprint, request, flash, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import os
from app import db
from models import File
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'csv'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 MB

UPLOAD_FOLDER = 'app/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

files = Blueprint("files", __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@files.route("/upload", methods=["POST"])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{secure_filename(file.filename)}"
        file.seek(0, os.SEEK_END)
        if file.tell() > MAX_FILE_SIZE:
            flash('File exceeds maximum allowed size of 16MB', 'danger')
            return redirect(request.url)
        file.seek(0)

        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        new_file = File(filename=filename, filepath=file_path, user_id=current_user.id)
        db.session.add(new_file)
        db.session.commit()

        flash('File uploaded successfully!', 'success')
        return redirect(url_for('files.view_files'))
    
    flash('File type not allowed or invalid', 'danger')
    return redirect(request.url)

@files.route("/view")
@login_required
def view_files():
    user_files = File.query.filter_by(user_id=current_user.id).all()
    return render_template("files.html", files=user_files)

@files.route("/delete/<int:file_id>", methods=["GET"])
@login_required
def delete_file(file_id):
    file_record = File.query.get_or_404(file_id)
    if file_record.user_id != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for('files.view_files'))
    
    try:
        os.remove(file_record.filepath)
        db.session.delete(file_record)
        db.session.commit()
        flash("File deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting file: {e}", "danger")
    
    return redirect(url_for('files.view_files'))

@files.route("/uploads/<filename>")
@login_required
def get_uploaded_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except Exception as e:
        flash(f"Error fetching file: {e}", "danger")
        return redirect(url_for('files.view_files'))
