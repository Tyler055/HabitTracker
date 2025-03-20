from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import db, Message  # Importing once at the top of the file to avoid circular import

chat = Blueprint('chat', __name__)

# Route for displaying the chat interface
@chat.route('/')
def chat_index():
    # Fetch messages from the database
    messages = Message.query.all()
    return render_template('chat.html', messages=messages)

# Route for sending a new message
@chat.route('/send', methods=['POST'])
def send_message():
    message = request.form['message']
    if message:
        # Create and save the new message in the database
        new_message = Message(content=message)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('chat.chat_index'))
    return 'Message is empty', 400

# Route for fetching messages (as JSON)
@chat.route('/get_messages')
def get_messages():
    # Fetch all messages from the database and return as JSON
    messages = Message.query.all()
    return jsonify([message.content for message in messages])  # Only send message content as JSON
