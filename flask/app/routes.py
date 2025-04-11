# routes.py
from flask import Blueprint, request, jsonify, session
from app import socketio

main_blueprint = Blueprint('main', __name__)

users = []  # This will store the players' information
is_game_started = False  # Flag to check if the game has started
sid_to_username = {}


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    global users, is_game_started

    print(f"Socket disconnected: {sid}")
    if not is_game_started:
        user = next((u for u in users if u['sid'] == sid), None)
        if user:
            print(f"User {user['username']} disconnected.")
            users = [u for u in users if u['sid'] != sid]
            socketio.emit('update_players', {'players': users})
    else:
        # Handle game disconnection logic here if needed
        print(f"User {sid} disconnected during the game.")


@main_blueprint.route('/join', methods=['POST'])
def join_game():
    global users, is_game_started
    data = request.get_json()
    username = data.get('username')
    color = data.get('color')
    sid = data.get('sid')

    if username and color:
        # Check if the user already exists
        for user in users:
            if user['username'] == username:
                return jsonify({"success": False, "error": "Username already taken"}), 400
        session['username'] = username  # Store the username in session
        session['color'] = color  # Store the color in session
        print(f"User {username} with color {color} joined the game.")
        if is_game_started:
            # If the game has started, send the current game state to the new player
            socketio.emit('game_state', {'players': users}, room=username)
        users.append({'username': username, 'color': color, 'sid': sid})

        # Broadcast the updated players list to all connected clients
        socketio.emit('update_players', {'players': users})
        
        return jsonify({"success": True, "players": users}), 200
    print("Missing username or color.")
    return jsonify({"success": False, "error": "Missing username or color"}), 400

@main_blueprint.route('/start-game', methods=['POST'])
def start_game():
    global is_game_started
    if is_game_started:
        return jsonify({"success": False, "error": "Game already started"}), 400
    # Generate random positions for players on the board
    positions = []
    for player in users:
        # Random positions on the board (you can adjust this to your game's board logic)
        positions.append({
            'username': player['username'],
            'top': 0,  # Example top position on the board
            'left': 0,  # Example left position on the board
        })
    
    # Broadcast the starting positions to all connected clients
    socketio.emit('start_game', {'positions': positions})
    is_game_started = True
    print("Game started with positions:", positions)    
    return jsonify({
        'success': True,
        'positions': positions
    }), 200


@main_blueprint.route('/reconnect', methods=['POST'])
def reconnect_game():
    global users
    global is_game_started

    print("\n--- /reconnect called ---")
    print(f"Game started? {is_game_started}")

    # Print all headers and cookies for inspection
    print("Request Headers:", dict(request.headers))
    print("Request Cookies:", request.cookies)
    print("Session contents:", dict(session))

    if is_game_started:
        username = session.get('username')
        color = session.get('color')

        print(f"Session username: {username}")
        print(f"Session color: {color}")

        if username and color:
            print("Reconnection successful.")
            return jsonify({
                "success": True,
                "username": username,
                "color": color
            }), 200

        print("No active session found.")
        return jsonify({"success": False, "error": "No active session"}), 400
    else:
        print("Game not started yet.")
        return jsonify({
            "success": True,
            "game_started": False,
            "error": "Game not started"
        }), 200



