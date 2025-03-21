from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Habit, ActivityLog

# Create a Blueprint for dashboard-related routes
dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/")
@login_required
def home():
    """Display the user dashboard with habit tracking and stats."""
    # Fetch all habits and the latest activity logs for the logged-in user
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    activities = ActivityLog.query.filter_by(user_id=current_user.id).order_by(ActivityLog.timestamp.desc()).limit(10).all()
    
    return render_template("dashboard.html", habits=habits, activities=activities)

