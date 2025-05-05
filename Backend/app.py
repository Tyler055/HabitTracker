import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import TemplateNotFound
from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired
from dataservice import (
    init_db, create_user, find_user_by_username, find_user_by_email,
    get_goals_by_category, save_goals_for_category, reset_all_goals,
    find_user_by_id, update_user_password, update_goal, clear_notifications,
    create_notification, get_notifications
)

# ─── Flask App Configuration ─────────────────────────────────
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'WebApp', 'templates')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'WebApp', 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = os.urandom(24)  # Use a secure fixed key in production

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

# ─── Forms ───────────────────────────────────────────────────
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])

# ─── Initialize Database ─────────────────────────────────────
with app.app_context():
    init_db()

# ─── Login Guard ─────────────────────────────────────────────
@app.before_request
def check_login_required():
    endpoint = request.endpoint or ''
    if not session.get('user_id') and endpoint not in {'signup', 'login', 'static', 'forgot_password'} and not endpoint.startswith('api'):
        return redirect(url_for('login'))

# ─── Routes ──────────────────────────────────────────────────

@app.route('/')
def habit_tracker():
    return render_template('habit.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form.get('email')
        password = request.form['password']
        password_confirm = request.form.get('password_confirm')

        if not username or not password:
            flash('Username and password are required.')
        elif password != password_confirm:
            flash('Passwords must match.')
        elif find_user_by_username(username):
            flash(f'Username {username} is already taken.')
        elif email and find_user_by_email(email):
            flash(f'Email {email} is already registered.')
        else:
            create_user(username, password, email)
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
    return render_template('auth.html', action='signup')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']
        user = find_user_by_username(identifier) or find_user_by_email(identifier)

        if not user or not check_password_hash(user['password'], password):
            flash('Invalid credentials.')
        else:
            session['user_id'] = user['id']
            return redirect(url_for('habit_tracker'))
    return render_template('auth.html', action='login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/notifications', methods=['GET', 'POST'])
def notifications():
    user_id = session['user_id']
    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            create_notification(user_id, message)
            flash('Notification created!')
            return redirect(url_for('notifications'))
    notifs = get_notifications(user_id)
    return render_template('notifications.html', notifications=notifs)

@app.route('/notifications/clear', methods=['POST'])
def clear_all_notifications():
    clear_notifications(session['user_id'])
    flash("Notifications cleared.")
    return redirect(url_for('notifications'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = find_user_by_id(session['user_id'])
        if not check_password_hash(user['password'], form.old_password.data):
            flash('Old password is incorrect.')
        elif form.new_password.data != form.confirm_password.data:
            flash('New passwords do not match.')
        else:
            update_user_password(user['id'], form.new_password.data)
            flash('Password updated successfully.')
            return redirect(url_for('profile'))
    return render_template('profile.html', form=form)

@app.route('/goals/<category>')
def goals_page(category):
    try:
        goals = get_goals_by_category(session['user_id'], category)
        return render_template(f'{category}.html', goals=goals)
    except TemplateNotFound:
        return "Category not found", 404

@app.route('/goals/all-goals')
def all_goals_page():
    user_id = session['user_id']
    return render_template('all-goals.html',
        daily_goals=get_goals_by_category(user_id, 'daily'),
        weekly_goals=get_goals_by_category(user_id, 'weekly'),
        monthly_goals=get_goals_by_category(user_id, 'monthly'),
        yearly_goals=get_goals_by_category(user_id, 'yearly')
    )

@app.route('/update_goal/<int:goal_id>', methods=['POST'])
def update_goal_route(goal_id):
    new_text = request.form['new_text']
    new_completed = request.form.get('new_completed') == 'true'
    result = update_goal(goal_id, new_text, new_completed)
    flash(result)
    return redirect(url_for('habit_tracker'))

# ─── API Routes ──────────────────────────────────────────────

@app.route('/api/goals', methods=['GET', 'POST'])
def api_goals():
    user_id = session['user_id']
    category = request.args.get('category')
    if request.method == 'GET':
        goals = get_goals_by_category(user_id, category)
        return jsonify([{'text': g['text'], 'completed': bool(g['completed'])} for g in goals])
    else:
        data = request.get_json()
        save_goals_for_category(user_id, category, data.get('goals', []))
        return jsonify({'message': 'Goals saved successfully'})

@app.route('/api/reset', methods=['POST'])
def reset_goals_api():
    reset_all_goals(session['user_id'])
    return jsonify({'message': 'Goals reset successfully'})

@app.route('/advanced')
def get_advanced_data():
    return jsonify({'message': 'Advanced data goes here'})

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = find_user_by_email(email)
        if user:
            flash('Password reset email sent (not implemented).')
        else:
            flash('Email not found.')
    return render_template('forgot_password.html')

# ─── Error Handling ──────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

# ─── Run the App ─────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
