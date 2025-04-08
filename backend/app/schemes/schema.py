from flask import current_app
from flask_mail import Message
from app.utils.extensions import mail
from marshmallow import Schema, fields, validate
import logging

# Function to send an email using Flask-Mail
def send_email(to: str, subject: str, body: str):
    """
    Sends an email using Flask-Mail.
    """
    logger = current_app.logger if current_app else logging.getLogger(__name__)
    try:
        if not current_app:
            raise RuntimeError("Flask application context is required to send emails.")
        if not hasattr(current_app, 'mail'):
            raise RuntimeError("Mail instance not initialized.")

        msg = Message(subject=subject, recipients=[to], body=body)
        mail.send(msg)

        logger.info(f"✅ Email sent to {to} with subject: {subject}")
    except Exception as e:
        logger.error(f"⚠️ Error sending email to {to} with subject {subject}: {e}")
        raise  # Optional

# Schema to validate habit data using Marshmallow
class HabitSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    frequency = fields.Str(
        required=False,
        load_default="daily",
        validate=validate.OneOf(["daily", "weekly", "monthly"])
    )

# Initialize the schema
habit_schema = HabitSchema()
habits_schema = HabitSchema(many=True)  # This defines a list of habits
