from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import secrets
from datetime import timedelta

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(16)
    
    # Configure CORS with explicit settings
    CORS(app, 
         supports_credentials=True,
         resources={
             r"/*": {
                 "origins": ["http://localhost:3000"],
                 "allow_headers": ["Content-Type"],
                 "methods": ["GET", "POST", "OPTIONS"]
             }
         })
    
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_COOKIE_SECURE'] = False  # For development only
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Helps with cross-origin cookies
    
    socketio.init_app(app, 
                     cors_allowed_origins="http://localhost:3000",
                     manage_session=False)  # Let Flask handle sessions
    
    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app, socketio