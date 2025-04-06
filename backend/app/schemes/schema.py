# schema.py

from flask import current_app
from flask_mail import Message
from app.utils.extensions import mail
from marshmallow import Schema, fields, validate

# Function to send an email using Flask-Mail
def send_email(to: str, subject: str, body: str):
    """
    Sends an email using Flask-Mail.

    Parameters:
    to (str): The recipient's email address.
    subject (str): The subject of the email.
    body (str): The body/content of the email.
    """
    try:
        # Ensure the Flask app context is available
        if not current_app:
            raise RuntimeError("Flask application context is required to send emails.")
        
        # Ensure Flask-Mail has been initialized
        if not hasattr(current_app, 'mail'):
            raise RuntimeError("Mail instance not initialized. Make sure mail.init_app(app) is called in create_app().")

        # Create and send the email
        msg = Message(subject=subject, recipients=[to], body=body)
        mail.send(msg)  # Sending email through Flask-Mail
        
        # Log success
        current_app.logger.info(f"✅ Email sent to {to} with subject: {subject}")
    except Exception as e:
        # Log any errors if they occur
        current_app.logger.error(f"⚠️ Error sending email to {to} with subject {subject}: {e}")


# Schema to validate habit data using Marshmallow
class HabitSchema(Schema):
    """
    Schema to validate the habit data.
    """
    name = fields.String(required=True, validate=validate.Length(min=1))
    description = fields.String(required=False, allow_none=True)
    frequency = fields.String(
        required=False,
        missing="daily",  # Default value if not provided
        validate=validate.OneOf(["daily", "weekly", "monthly"])  # Valid values
    )

# Initialize the schema
habit_schema = HabitSchema()
