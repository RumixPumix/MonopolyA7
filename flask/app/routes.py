# routes.py
from flask import Blueprint, request, jsonify
from app import socketio

main_blueprint = Blueprint('main', __name__)

users = []  # This will store the players' information

@main_blueprint.route('/join', methods=['POST'])
def join_game():
    data = request.get_json()
    username = data.get('username')
    color = data.get('color')

    if username and color:
        print("Success")
        users.append({'username': username, 'color': color})

        # Broadcast the updated players list to all connected clients
        socketio.emit('update_players', {'players': users})
        
        return jsonify({"success": True, "players": users}), 200
    print("Failed")
    return jsonify({"success": False, "error": "Missing username or color"}), 400
