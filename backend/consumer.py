from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'dht-data',
    bootstrap_servers='localhost:29092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Consumer started...")

for message in consumer:
    print("Received:", message.value)
