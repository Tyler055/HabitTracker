from flask import current_app
from flask_mail import Message
from app.extensions import mail

def send_email(to: str, subject: str, body: str):
    """
    A function to send emails using Flask-Mail.
    """
    try:
        msg = Message(subject=subject, recipients=[to])
        msg.body = body  # Text content of the email
        mail.send(msg)
        print(f"Email sent to {to} with subject: {subject}")
    except Exception as e:
        print(f"Error sending email: {e}")
