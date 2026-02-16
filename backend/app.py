import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from upstash_redis import Redis
import json
import threading
import time
import os

# Configuration: Supports both custom and Upstash-provided env var names
REDIS_URL = os.getenv('REDIS_REST_URL') or os.getenv('UPSTASH_REDIS_REST_URL') or 'https://quality-mosquito-57744.upstash.io'
REDIS_TOKEN = os.getenv('REDIS_REST_TOKEN') or os.getenv('UPSTASH_REDIS_REST_TOKEN') or 'AeGQAAIncDJmZTZjODc4YmYwZjU0MmJiODg3Y2IxMzM3YWUyYWYxNHAyNTc3NDQ'
# Define a Secret Key for Sensor Authentication
SENSOR_API_KEY = "iot_secure_key_2024_v1"

CHANNEL_NAME = 'dht-stream'

app = Flask(__name__)

# Security: Reverting to broad CORS for debugging and ensuring connectivity
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet', logger=True, engineio_logger=True)

# Initialize Upstash Redis REST client
redis_client = Redis(url=REDIS_URL, token=REDIS_TOKEN)

@app.route('/')
def home():
    print("Home endpoint hit")
    return "IoT Backend is Online - Debug Mode", 200

@app.route('/sensor', methods=['POST', 'GET'])
def sensor_data():
    if request.method == 'GET':
        return "Sensor endpoint active", 200
    # 1. SECURITY CHECK: Validate Secret API Key
    api_key = request.headers.get('X-API-KEY')
    if api_key != SENSOR_API_KEY:
        print("Unauthorized access attempt blocked.")
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400
    
    try:
        # Publish to Redis and Broadcast to Dashboard
        redis_client.publish(CHANNEL_NAME, json.dumps(data))
        socketio.emit('sensor_data', data)
        print(f"Relayed secure data: {data}")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Server starting on port {port}...")
    socketio.run(app, host='0.0.0.0', port=port)
