from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import redis
import json
import threading
import time
import os

# Configuration
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
# Upstash specific (if URL isn't used)
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

CHANNEL_NAME = 'dht-stream'

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

def get_redis_client():
    try:
        if REDIS_HOST and REDIS_PASSWORD:
            return redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASSWORD,
                decode_responses=True
            )
        return redis.from_url(REDIS_URL, decode_responses=True)
    except Exception as e:
        print(f"Redis connection error: {e}")
        return None

@app.route('/sensor', methods=['POST', 'GET'])
def sensor_data():
    if request.method == 'GET':
        return "Backend is running!", 200
        
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400
    
    r = get_redis_client()
    if r:
        try:
            # Publish to Redis channel
            r.publish(CHANNEL_NAME, json.dumps(data))
            print(f"Received from sensor: {data}")
            return jsonify({"status": "success"}), 200
        except Exception as e:
            print(f"Redis Publish fail: {e}")
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Redis not available"}), 503

def redis_listener():
    print("Redis listener thread started")
    while True:
        try:
            r = get_redis_client()
            if r:
                pubsub = r.pubsub()
                pubsub.subscribe(CHANNEL_NAME)
                print(f"Subscribed to Redis channel: {CHANNEL_NAME}")
                
                for message in pubsub.listen():
                    if message['type'] == 'message':
                        try:
                            data = json.loads(message['data'])
                            print(f"Broadcasting to Dashboard: {data}")
                            socketio.emit('sensor_data', data)
                        except Exception as e:
                            print(f"Data error: {e}")
            else:
                print("Waiting for Redis...")
                time.sleep(5)
        except Exception as e:
            print(f"Redis listener error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    # Start Redis listener thread
    thread = threading.Thread(target=redis_listener, daemon=True)
    thread.start()
    
    port = int(os.environ.get('PORT', 5000))
    print(f"Server starting on port {port}...")
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
