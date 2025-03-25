from flask import Flask, render_template, request, redirect, url_for, g, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__, template_folder="templates")

# Function to get the database connection
def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host="localhost",
                user="knight0",  # Replace with your MySQL username
                password="",  # Replace with your MySQL password
                database="habit_tracker"  # Replace with your DB name
            )
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            raise e
    return g.db

# Function to close the database connection
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Route to Display Habits
@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM habits")
    habits = cursor.fetchall()
    return render_template('index.html', habits=habits)

# Route to Add a Habit
@app.route('/add', methods=['POST'])
def add_habit():
    habit_name = request.form['habit_name']
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO habits (name) VALUES (%s)", (habit_name,))
        db.commit()
    except Error as e:
        print(f"Error inserting habit: {e}")
        db.rollback()
    return redirect(url_for('index'))

# Route to Delete a Habit
@app.route('/delete/<int:habit_id>', methods=['GET'])
def delete_habit(habit_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM habits WHERE id = %s", (habit_id,))
        db.commit()
    except Error as e:
        print(f"Error deleting habit: {e}")
        db.rollback()
    return redirect(url_for('index'))

# Route to Reset Habits (called from JavaScript)
@app.route('/reset_habits', methods=['POST'])
def reset_habits():
    # Reset habits to the base form (default habits)
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM habits")  # Clear existing habits
        db.commit()

        # Add default habits
        default_habits = ['Drink Water', 'Exercise', 'Read', 'Sleep Well']
        for habit in default_habits:
            cursor.execute("INSERT INTO habits (name) VALUES (%s)", (habit,))
        db.commit()

        return jsonify(success=True)
    except Error as e:
        print(f"Error resetting habits: {e}")
        db.rollback()
        return jsonify(success=False)

if __name__ == '__main__':
    app.run(debug=True)
