from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Habit, ActivityLog
from sqlalchemy import func

# Create a Blueprint for dashboard-related routes
dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/")
@login_required
def home():
    """Display the user dashboard with habit tracking and stats."""
    # Fetch all habits for the logged-in user
    habits = Habit.query.filter_by(user_id=current_user.id).all()

    # Fetch the latest activity logs for the logged-in user (limit to 10)
    activities = ActivityLog.query.filter_by(user_id=current_user.id).order_by(ActivityLog.timestamp.desc()).limit(10).all()

    # Example: Calculate the number of completed habits for display
    completed_habits_count = Habit.query.filter_by(user_id=current_user.id, is_completed=True).count()

    # If no activities or habits, display appropriate message in the template
    if not habits:
        habits_message = "You haven't added any habits yet!"
    else:
        habits_message = None

    if not activities:
        activities_message = "No recent activities found!"
    else:
        activities_message = None

    return render_template(
        "dashboard.html", 
        habits=habits, 
        activities=activities, 
        completed_habits_count=completed_habits_count,
        habits_message=habits_message,
        activities_message=activities_message
    )
