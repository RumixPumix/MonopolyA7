from flask import Flask, request, jsonify  # Add 'request' and 'jsonify' to imports
from flask_socketio import SocketIO
from flask_cors import CORS
import secrets
from datetime import timedelta

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_hex(32)
    
    # Configure CORS with explicit settings
    CORS(app,
         resources={
             r"/*": {
                 "origins": ["http://localhost:3000"],
                 "methods": ["GET", "POST", "OPTIONS"],
                 "allow_headers": ["Content-Type"],
                 "supports_credentials": True,
                 "expose_headers": ["Content-Type"]
             }
         })
    
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    socketio.init_app(app,
                     cors_allowed_origins="http://localhost:3000",
                     manage_session=False,
                     engineio_logger=True,
                     logger=True)

    # ===== ADD THE PREFLIGHT HANDLER HERE =====
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = jsonify({"status": "preflight"})
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
            response.headers.add("Access-Control-Allow-Headers", "*")
            response.headers.add("Access-Control-Allow-Methods", "*")
            response.headers.add("Access-Control-Allow-Credentials", "true")
            return response
    # =========================================

    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app, socketio