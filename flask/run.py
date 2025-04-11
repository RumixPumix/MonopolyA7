# run.py
from app import create_app

# Create the app and get both Flask app and socketio instance
app, socketio = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)  # Start the app with SocketIO
