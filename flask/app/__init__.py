# app/__init__.py
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS  # Import CORS
import secrets

socketio = SocketIO()  # Initialize SocketIO

def create_app():
    app = Flask(__name__)  # Initialize Flask app
    app.secret_key = secrets.token_hex(16)
    # Enable CORS for all routes and SocketIO
    CORS(app, supports_credentials=True)  # This will allow all domains, adjust the origins if needed
    
    # Initialize SocketIO with the Flask app
    socketio.init_app(app, cors_allowed_origins="*")  # Allow cross-origin requests for SocketIO
    
    # Import the routes and register the blueprint
    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app, socketio  # Return both app and socketio instances
