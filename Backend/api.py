# api.py

from flask import Blueprint, request, jsonify, session
from dataservice import get_goals_by_category, save_goals_for_category, reset_all_goals

api_bp = Blueprint('api', __name__)

@api_bp.route('/goals', methods=['GET', 'POST'])
def api_goals():
    user_id = session['user_id']
    category = request.args.get('category')

    if request.method == 'GET':
        goals = get_goals_by_category(user_id, category)
        return jsonify([{'text': g['text'], 'completed': bool(g['completed'])} for g in goals])

    data = request.get_json()
    save_goals_for_category(user_id, category, data.get('goals', []))
    return jsonify({'message': 'Goals saved successfully'})

@api_bp.route('/reset', methods=['POST'])
def reset_goals_api():
    reset_all_goals(session['user_id'])
    return jsonify({'message': 'Goals reset successfully'})