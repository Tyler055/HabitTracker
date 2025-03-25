from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from models import db, Message  # Importing once at the top of the file to avoid circular import
from datetime import datetime

chat = Blueprint('chat', __name__)

# Route for displaying the chat interface
@chat.route('/')
def chat_index():
    # Fetch messages from the database, ordered by timestamp (if it exists)
    messages = Message.query.order_by(Message.timestamp.asc()).all()
    return render_template('chat.html', messages=messages)

# Route for sending a new message
@chat.route('/send', methods=['POST'])
def send_message():
    message = request.form['message']
    if message:
        # Create and save the new message in the database
        new_message = Message(content=message, timestamp=datetime.utcnow())  # Add timestamp
        db.session.add(new_message)
        db.session.commit()
        flash('Message sent!', 'success')  # Flash message to user
        return redirect(url_for('chat.chat_index'))
    else:
        flash('Message cannot be empty!', 'danger')  # Flash error if the message is empty
        return redirect(url_for('chat.chat_index'))

# Route for fetching messages (as JSON)
@chat.route('/get_messages')
def get_messages():
    # Fetch all messages from the database and return as JSON
    messages = Message.query.order_by(Message.timestamp.asc()).all()
    return jsonify([{'content': message.content, 'timestamp': message.timestamp} for message in messages])  # Include timestamp for context
