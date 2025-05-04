import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from dataservice import (
    init_db,
    create_user,
    find_user_by_username,
    find_user_by_email,
    get_goals_by_category,
    save_goals_for_category,
    reset_all_goals
)
from jinja2 import TemplateNotFound

# Set project paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'WebApp', 'templates')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'WebApp', 'static')

# Create Flask app
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = os.urandom(24)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

# Initialize DB once at startup
with app.app_context():
    init_db()

@app.before_request
def check_login_required():
    if not session.get('user_id') and request.endpoint not in {'signup', 'login', 'static'} and not request.endpoint.startswith('api'):
        return redirect(url_for('login'))

# ─────── Routes ───────────────────────────────────────────

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form.get('email')
        password = request.form['password']

        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif find_user_by_username(username) is not None:
            error = f'User {username} is already registered.'

        if error is None:
            try:
                hashed_password = generate_password_hash(password)
                create_user(username, hashed_password, email)
                flash('Registration successful! Please log in.')
                return redirect(url_for('login'))
            except Exception as e:
                flash(f'Error creating user: {e}')
        else:
            flash(error)

    return render_template('auth.html', action='signup')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']

        user = find_user_by_username(identifier) or find_user_by_email(identifier)

        if user is None:
            flash('User not found.')
        elif not check_password_hash(user['password'], password):
            flash('Incorrect password.')
        else:
            session['user_id'] = user['id']
            return redirect(url_for('habit_tracker'))

    return render_template('auth.html', action='login')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/')
def habit_tracker():
    return render_template('habit.html')

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

@app.route('/api/goals', methods=['GET', 'POST'])
def api_goals():
    user_id = session['user_id']
    category = request.args.get('category')

    if request.method == 'GET':
        goals = get_goals_by_category(user_id, category)
        return jsonify([{'text': row['text'], 'completed': bool(row['completed'])} for row in goals])
    elif request.method == 'POST':
        data = request.get_json()
        goals = data.get('goals', [])
        save_goals_for_category(user_id, category, goals)
        return jsonify({'message': 'Goals saved successfully'})

@app.route('/api/reset', methods=['POST'])
def reset_goals_api():
    reset_all_goals(session['user_id'])
    return jsonify({'message': 'Goals reset successfully'})

@app.route('/advanced', methods=['GET'])
def get_advanced_data():
    return jsonify({"message": "Advanced data goes here"})
@app.route('/profile', methods=['GET'])
def profile():
    user_id = session['user_id']
    user = find_user_by_username(user_id)
    return render_template('profile.html', user=user)
           
@app.route('/settings', methods=['GET'])
def settings():
    return render_template('settings.html')

@app.route('/forgot-password')
def forgot_password():
    return "Forgot password page coming soon!"


if __name__ == '__main__':
    app.run(debug=True)
