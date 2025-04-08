from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import Habit, ActivityLog

# Create a Blueprint for habit-related routes
habits = Blueprint("habits", __name__)

@habits.route("/")
@login_required
def view_habits():
    """Display all habits for the logged-in user."""
    page = request.args.get('page', 1, type=int)
    user_habits = Habit.query.filter_by(user_id=current_user.id).paginate(page, per_page=10)
    return render_template("habits.html", habits=user_habits)

@habits.route("/add", methods=["POST"])
@login_required
def add_habit():
    """Add a new habit."""
    name = request.form.get("name")
    if name:
        # Ensure habit name is unique
        if Habit.query.filter_by(user_id=current_user.id, name=name).first():
            flash("This habit already exists.", "danger")
        else:
            new_habit = Habit(name=name, user_id=current_user.id)
            db.session.add(new_habit)
            db.session.commit()
            flash("Habit added successfully!", "success")
    else:
        flash("Habit name cannot be empty.", "danger")
    
    return redirect(url_for("habits.view_habits"))

@habits.route("/delete/<int:habit_id>")
@login_required
def delete_habit(habit_id):
    """Delete a habit by ID."""
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for("habits.view_habits"))
    
    db.session.delete(habit)
    db.session.commit()
    flash("Habit deleted successfully!", "success")
    
    return redirect(url_for("habits.view_habits"))

@habits.route("/complete/<int:habit_id>")
@login_required
def complete_habit(habit_id):
    """Mark a habit as completed and update the streak."""
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for("habits.view_habits"))
    
    # Update streak or completion logic
    habit.update_streak()
    db.session.commit()
    flash(f"Great job! You completed '{habit.name}'.", "success")
    
    # Log the activity (optional, if you want to track completion)
    activity_log = ActivityLog(user_id=current_user.id, habit_id=habit.id, action="completed")
    db.session.add(activity_log)
    db.session.commit()
    
    return redirect(url_for("habits.view_habits"))
