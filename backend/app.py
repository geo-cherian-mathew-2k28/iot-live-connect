import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Optimized for lightning-fast real-time sync
socketio = SocketIO(
    app, 
    cors_allowed_origins="*", 
    async_mode='eventlet',
    ping_timeout=10,
    ping_interval=5
)

SENSOR_API_KEY = "iot_secure_key_2024_v1"

@app.route('/')
def health():
    return "IoT-Secure-Relay: Online", 200

@app.route('/sensor', methods=['POST'])
def sensor_data():
    api_key = request.headers.get('X-API-KEY')
    if api_key != SENSOR_API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400
    
    # IMMEDIATE RELAY (Zero Latency)
    socketio.emit('sensor_data', data)
    
    # Instant Success Response to ESP32
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    socketio.run(app, host='0.0.0.0', port=port)
