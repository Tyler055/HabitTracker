from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from jinja2 import TemplateNotFound
from dataservice import get_goals_by_category, save_goals_for_category, reset_all_goals, create_notification, get_notifications, clear_notifications

# Create a new blueprint for views
views_bp = Blueprint('views', __name__)

# Route for the habit tracker page (index)
@views_bp.route('/')
def habit_tracker():
    if 'user_id' not in session:
        flash("Please log in first", "warning")
        return redirect(url_for('auth.login'))
    return render_template('habit.html')

# Route for the advanced goals page
@views_bp.route('/advanced')
def get_advanced_data():
    user_id = session['user_id']
    category = request.args.get('category')
    try:
        goals = get_goals_by_category(user_id, category)
        return render_template('advanced.html', category=category, goals=goals)
    except Exception as e:
        flash(f"Error retrieving goals for {category}: {str(e)}", 'error')
        return redirect(url_for('views.habit_tracker'))

# Route for the settings page
@views_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' not in session:
        flash("Please log in first", "warning")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            create_notification(user_id, message)
            flash('Notification created!', 'success')
            return redirect(url_for('views.settings'))
        else:
            flash('Message cannot be empty', 'error')

    notifications = get_notifications(user_id)
    return render_template('settings.html', notifications=notifications)

# Route to clear all notifications for the user
@views_bp.route('/settings/notifications/clear', methods=['POST'])
def clear_all_notifications():
    if 'user_id' not in session:
        flash("Please log in first", "warning")
        return redirect(url_for('auth.login'))

    clear_notifications(session['user_id'])
    flash("Notifications cleared.", 'info')
    return redirect(url_for('views.settings'))

# Route to render the goals page based on the category
@views_bp.route('/goals/<category>')
def goals_page(category):
    if 'user_id' not in session:
        flash("Please log in first", "warning")
        return redirect(url_for('auth.login'))

    try:
        goals = get_goals_by_category(session['user_id'], category)
        return render_template(f'{category}.html', goals=goals)
    except TemplateNotFound:
        flash(f"Category '{category}' not found", 'error')
        return redirect(url_for('views.habit_tracker'))

# Route to display all goals across all categories
@views_bp.route('/goals/all-goals')
def all_goals_page():
    if 'user_id' not in session:
        flash("Please log in first", "warning")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    return render_template('all-goals.html',
        daily_goals=get_goals_by_category(user_id, 'daily'),
        weekly_goals=get_goals_by_category(user_id, 'weekly'),
        monthly_goals=get_goals_by_category(user_id, 'monthly'),
        yearly_goals=get_goals_by_category(user_id, 'yearly')
    )
