import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from dataservice import (
    init_db,
    create_user,
    find_user_by_username,
    get_goals_by_category,
    save_goals_for_category,
    reset_all_goals
)

# Project structure setup
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'WebApp', 'templates')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'WebApp', 'static')

# Flask app setup
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# Secret key setup (for development only, should be fixed in production)
app.secret_key = os.urandom(24)  # Generates a new key on each server start

# ─────── Before Request ──────────────────────────────

@app.before_request
def before_request():
    init_db()  # Ensures database is initialized
    if not session.get('user_id') and request.endpoint not in ['signup', 'login', 'static']:
        return redirect(url_for('login'))

# ─────── Authentication ──────────────────────────────

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif find_user_by_username(username):
            error = f'User "{username}" is already registered.'

        if error is None:
            create_user(username, password)
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))

        flash(error)

    return render_template('auth.html', action='signup')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = find_user_by_username(username)

        if user is None:
            flash('Incorrect username.')
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

# ─────── Main Pages ──────────────────────────────────

@app.route('/')
def habit_tracker():
    return render_template('habit.html')

@app.route('/goals/<category>')
def goals_page(category):
    goals = get_goals_by_category(session['user_id'], category)
    return render_template(f'{category}.html', goals=goals)

@app.route('/goals/all-goals')
def all_goals_page():
    daily_goals = get_goals_by_category(session['user_id'], 'daily')
    weekly_goals = get_goals_by_category(session['user_id'], 'weekly')
    monthly_goals = get_goals_by_category(session['user_id'], 'monthly')
    yearly_goals = get_goals_by_category(session['user_id'], 'yearly')
    return render_template('all-goals.html', daily_goals=daily_goals, weekly_goals=weekly_goals, monthly_goals=monthly_goals, yearly_goals=yearly_goals)

# ─────── API Endpoints ───────────────────────────────

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

# ─────── Run Server ──────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True)
