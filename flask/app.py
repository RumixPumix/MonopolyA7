# app.py
from flask import Flask
from flask_socketio import SocketIO

def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app)  # Initialize SocketIO

    # Import routes after app is created to avoid circular imports
    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app, socketio
