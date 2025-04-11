from flask import Blueprint, request, jsonify, session
from app import socketio
from flask_socketio import join_room, leave_room

main_blueprint = Blueprint('main', __name__)

users = []
is_game_started = False
username_to_sid = {}

# SocketIO event handlers
@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")
    if 'username' in session:
        username = session['username']
        print(f"User {username} reconnected with new SID: {request.sid}")
        username_to_sid[username] = request.sid
        join_room(username)
        # Update the user's SID in the users list
        for user in users:
            if user['username'] == username:
                user['sid'] = request.sid
        socketio.emit('update_players', {'players': users})

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    global users, is_game_started

    print(f"Socket disconnected: {sid}")
    username = next((u['username'] for u in users if u['sid'] == sid), None)
    
    if username:
        if not is_game_started:
            print(f"User {username} disconnected before game start.")
            users = [u for u in users if u['sid'] != sid]
            socketio.emit('update_players', {'players': users})
        else:
            print(f"User {username} disconnected during game.")
            # Keep them in the users list but mark as disconnected if needed

@main_blueprint.route('/admin', methods=['POST', 'GET'])
def admin_panel():
    global users, is_game_started, username_to_sid
    return jsonify({
        "success": True,
        "message": "Admin panel is available at /admin",
        "users": users,
        "game_started": is_game_started,
        "username_to_sid": username_to_sid
    }), 200

# HTTP routes
@main_blueprint.route('/join', methods=['POST'])
def join_game():
    global users, is_game_started
    data = request.get_json()
    username = data.get('username')
    color = data.get('color')
    sid = data.get('sid')  # This should come from the client's socket connection

    if not username or not color:
        return jsonify({"success": False, "error": "Missing username or color"}), 400

    # Check if username exists but with different SID (reconnection case)
    existing_user = next((u for u in users if u['username'] == username), None)
    if existing_user:
        if existing_user['sid'] != sid:
            # Update the SID for reconnection
            existing_user['sid'] = sid
            username_to_sid[username] = sid
            session['username'] = username
            session['color'] = color
            return jsonify({"success": True, "players": users}), 200
        return jsonify({"success": False, "error": "Username already taken"}), 400

    # New user joining
    session['username'] = username
    session['color'] = color
    users.append({'username': username, 'color': color, 'sid': sid})
    username_to_sid[username] = sid
    
    socketio.emit('update_players', {'players': users})
    return jsonify({"success": True, "players": users}), 200

@main_blueprint.route('/start-game', methods=['POST'])
def start_game():
    global is_game_started
    if is_game_started:
        return jsonify({"success": False, "error": "Game already started"}), 400
    
    positions = []
    for player in users:
        positions.append({
            'username': player['username'],
            'top': 0,
            'left': 0,
        })
    
    socketio.emit('start_game', {'positions': positions})
    is_game_started = True
    return jsonify({'success': True, 'positions': positions}), 200

@main_blueprint.route('/reconnect', methods=['POST'])
def reconnect_game():
    if 'username' not in session:
        return jsonify({"success": False, "error": "No active session"}), 400
    
    username = session['username']
    color = session.get('color', '')
    
    return jsonify({
        "success": True,
        "username": username,
        "color": color,
        "game_started": is_game_started,
        "players": users
    }), 200