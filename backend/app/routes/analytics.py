# app/routes/analytics.py

from flask import Blueprint, jsonify, session
from pymongo import MongoClient
from datetime import datetime, timedelta
from collections import defaultdict

mongo_bp = Blueprint('mongo', __name__, url_prefix='/mongo')

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
mongo_db = client["habitdb"]
completions_collection = mongo_db["completions"]  # assumed collection for habit completions

# Utility to get today's date string
def today_str():
    return datetime.utcnow().date().isoformat()

# Route: Get total completions for current user
@mongo_bp.route('/total_completions', methods=['GET'])
def total_completions():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    username = session['username']
    total = completions_collection.count_documents({"username": username})

    return jsonify({"username": username, "total_completions": total}), 200

# Route: Get completion history (dates of completion per habit)
@mongo_bp.route('/history', methods=['GET'])
def completion_history():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    username = session['username']
    records = completions_collection.find({"username": username})

    history = defaultdict(list)
    for record in records:
        habit = record.get("habit")
        date_completed = record.get("date_completed")
        if habit and date_completed:
            history[habit].append(date_completed)

    return jsonify({"username": username, "history": history}), 200

# Route: Get current streak per habit
@mongo_bp.route('/streaks', methods=['GET'])
def habit_streaks():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    username = session['username']
    records = completions_collection.find({"username": username})

    habit_dates = defaultdict(set)
    for record in records:
        habit = record.get("habit")
        date_str = record.get("date_completed")
        if habit and date_str:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            habit_dates[habit].add(date_obj)

    streaks = {}
    for habit, dates in habit_dates.items():
        current_streak = 0
        today = datetime.utcnow().date()
        while today in dates:
            current_streak += 1
            today -= timedelta(days=1)
        streaks[habit] = current_streak

    return jsonify({"username": username, "streaks": streaks}), 200
