from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from upstash_redis import Redis
import json
import threading
import time
import os

# Configuration
# Use the REST URL and Token provided by Upstash
REDIS_URL = os.getenv('REDIS_REST_URL', 'https://quality-mosquito-57744.upstash.io')
REDIS_TOKEN = os.getenv('REDIS_REST_TOKEN', 'AeGQAAIncDJmZTZjODc4YmYwZjU0MmJiODg3Y2IxMzM3YWUyYWYxNHAyNTc3NDQ')

CHANNEL_NAME = 'dht-stream'

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Initialize Upstash Redis REST client
redis_client = Redis(url=REDIS_URL, token=REDIS_TOKEN)

@app.route('/sensor', methods=['POST', 'GET'])
def sensor_data():
    if request.method == 'GET':
        return "Backend is running!", 200
        
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400
    
    try:
        # Publish using REST - this is extremely reliable for cloud deployment
        redis_client.publish(CHANNEL_NAME, json.dumps(data))
        print(f"Received from sensor: {data}")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Upstash Error: {e}")
        return jsonify({"error": str(e)}), 500

def redis_listener():
    """
    Note: Upstash REST doesn't support the standard blocking .listen().
    For serverless, we usually use a small polling loop or a dedicated 
    Websocket if available. But since we are on Koyeb (24/7), we will 
    use a simple polling for new messages or a long-poll if supported.
    
    Alternatively, since the same app handles both, we can just 
    emit directly to SocketIO when data hits /sensor!
    This is much more efficient and avoids listeners entirely.
    """
    print("Direct broadcasting enabled.")

# Refined sensor endpoint for efficiency
@app.route('/sensor-relay', methods=['POST'])
def sensor_relay():
    data = request.json
    # 1. Store in Redis for history/reliability
    redis_client.publish(CHANNEL_NAME, json.dumps(data))
    # 2. Emit directly to dashboard (Fastest)
    socketio.emit('sensor_data', data)
    return jsonify({"status": "relayed"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Server starting on port {port}...")
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
