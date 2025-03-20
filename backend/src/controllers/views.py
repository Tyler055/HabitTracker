from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from models import get_db_connection

# Blueprint for views
views = Blueprint('views', __name__)

# Route: Show all habits
@views.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habits")  # Get all habits from the database
    habits = cursor.fetchall()  # Fetch all the results
    cursor.close()
    conn.close()
    return render_template('index.html', habits=habits)  # Pass habits to the template

# Route: Add a new habit
@views.route('/add', methods=['POST'])
def add_habit():
    habit_name = request.form['habit_name']  # Get habit name from the form
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO habits (name) VALUES (%s)", (habit_name,))  # Insert new habit
        conn.commit()  # Commit the transaction
        flash("Habit added successfully!", "success")  # Flash a success message
    except Exception as e:
        print(f"Error adding habit: {e}")
        conn.rollback()  # Rollback in case of error
        flash("Error adding habit. Please try again.", "error")  # Flash an error message
    cursor.close()
    conn.close()
    return redirect(url_for('views.index'))  # Redirect to the main page

# Route: Delete a habit
@views.route('/delete/<int:habit_id>', methods=['GET'])
def delete_habit(habit_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM habits WHERE id = %s", (habit_id,))  # Delete the habit by id
        conn.commit()  # Commit the transaction
        flash("Habit deleted successfully!", "success")  # Flash a success message
    except Exception as e:
        print(f"Error deleting habit: {e}")
        conn.rollback()  # Rollback in case of error
        flash("Error deleting habit. Please try again.", "error")  # Flash an error message
    cursor.close()
    conn.close()
    return redirect(url_for('views.index'))  # Redirect to the main page

# Route: Reset habits (called from JavaScript)
@views.route('/reset_habits', methods=['POST'])
def reset_habits():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM habits")  # Clear existing habits
        conn.commit()

        # Add default habits
        default_habits = ['Drink Water', 'Exercise', 'Read', 'Sleep Well']
        for habit in default_habits:
            cursor.execute("INSERT INTO habits (name) VALUES (%s)", (habit,))
        conn.commit()

        return jsonify(success=True)  # Return success response as JSON
    except Exception as e:
        print(f"Error resetting habits: {e}")
        conn.rollback()  # Rollback in case of error
        return jsonify(success=False)  # Return failure response as JSON
    finally:
        cursor.close()
        conn.close()

