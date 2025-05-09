from flask import Blueprint, request, jsonify, session, abort
from dataservice import get_goals_by_category, save_goals_for_category, reset_all_goals

api_bp = Blueprint('api', __name__)

# Utility function to check if user is logged in
def get_user_id_from_session():
    user_id = session.get('user_id')
    if not user_id:
        abort(401, description="User not logged in.")
    return user_id

@api_bp.route('/goals', methods=['GET', 'POST'])
def api_goals():
    user_id = get_user_id_from_session()  # Ensure user is logged in
    category = request.args.get('category')

    if request.method == 'GET':
        # Validate that category is provided in the query string
        if not category:
            return jsonify({'error': 'Category is required'}), 400
        
        # Retrieve goals for the given category
        goals = get_goals_by_category(user_id, category)
        return jsonify([{'text': g['text'], 'completed': bool(g['completed'])} for g in goals])

    # Handle POST request to save goals
    data = request.get_json()

    # Validate that goals is a list
    if not isinstance(data.get('goals', []), list):
        return jsonify({'error': 'Invalid goals format. Expected a list.'}), 400

    # Save goals for the given category
    save_goals_for_category(user_id, category, data.get('goals', []))
    return jsonify({'message': 'Goals saved successfully'}), 201  # Return 201 Created status

@api_bp.route('/reset', methods=['POST'])
def reset_goals_api():
    user_id = get_user_id_from_session()  # Ensure user is logged in
    reset_all_goals(user_id)  # Reset goals for the logged-in user
    return jsonify({'message': 'Goals reset successfully'}), 200  # Return 200 OK status
