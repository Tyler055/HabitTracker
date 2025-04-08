from flask import request, render_template, redirect, url_for, flash
from flask_mail import Message
from werkzeug.security import generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import app, db, mail
from models import User
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import PasswordField

# Create a password reset token
def generate_reset_token(email, expiration=3600):
    s = Serializer(app.config['SECRET_KEY'], expiration)
    return s.dumps({'email': email}).decode('utf-8')

# Verify the token
def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        email = s.loads(token)['email']
    except Exception:
        return None
    return email

# Route for requesting a password reset email
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate reset token and send reset email
            reset_token = generate_reset_token(user.email)
            reset_url = url_for('reset_with_token', token=reset_token, _external=True)
            msg = Message('Password Reset Request', sender='your_email@example.com', recipients=[user.email])
            msg.body = f'Click the following link to reset your password: {reset_url}'
            try:
                mail.send(msg)
                flash('Check your email for the password reset link!', 'info')
            except Exception as e:
                flash(f'Error sending email: {str(e)}', 'danger')
        else:
            flash('No account found with that email address.', 'danger')
    return render_template('auth/reset_password.html')

# Route for resetting the password with a valid token
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    email = verify_reset_token(token)
    if email is None:
        flash('The password reset token has expired or is invalid. Please request a new one.', 'danger')
        return redirect(url_for('auth.login'))

    # Password reset form
    class ResetPasswordForm(FlaskForm):
        new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
        confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        new_password = form.new_password.data
        user = User.query.filter_by(email=email).first()
        user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Password reset successful!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_with_token.html', form=form)
