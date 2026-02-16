import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from upstash_redis import Redis
import json
import os

# Configuration
REDIS_URL = os.getenv('REDIS_REST_URL') or os.getenv('UPSTASH_REDIS_REST_URL') or 'https://quality-mosquito-57744.upstash.io'
REDIS_TOKEN = os.getenv('REDIS_REST_TOKEN') or os.getenv('UPSTASH_REDIS_REST_TOKEN') or 'AeGQAAIncDJmZTZjODc4YmYwZjU0MmJiODg3Y2IxMzM3YWUyYWYxNHAyNTc3NDQ'
SENSOR_API_KEY = "iot_secure_key_2024_v1"

app = Flask(__name__)
# Professional CORS: Allow Vercel and WebSocket Handshakes
CORS(app, resources={r"/*": {"origins": "*"}})

# Professional SocketIO: Optimized for Cloud Proxies (Koyeb/Cloudflare)
socketio = SocketIO(
    app, 
    cors_allowed_origins="*", 
    async_mode='eventlet',
    engineio_logger=True,
    logger=True,
    always_connect=True,
    ping_timeout=60,
    ping_interval=25
)

redis_client = Redis(url=REDIS_URL, token=REDIS_TOKEN)

@app.route('/')
def health_check():
    return jsonify({"status": "healthy", "service": "IoT-Secure-Relay"}), 200

@app.route('/sensor', methods=['POST'])
def sensor_data():
    api_key = request.headers.get('X-API-KEY')
    if api_key != SENSOR_API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if not data:
        return jsonify({"error": "Bad Request"}), 400
    
    try:
        # Publish to Redis for Persistence
        redis_client.publish('dht-stream', json.dumps(data))
        # Real-time relay to Dashboard
        socketio.emit('sensor_data', data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        app.logger.error(f"Upstash Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    # When running locally or via python app.py
    port = int(os.environ.get('PORT', 8000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
