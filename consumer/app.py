from kafka import KafkaConsumer
from flask import Flask, jsonify
import json, os, threading

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
app = Flask(__name__)
message_log = []

def consume():
    consumer = KafkaConsumer(
        "events",
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        group_id="consumer-group"
    )
    for msg in consumer:
        print(f"Consumed: {msg.value}", flush=True)
        message_log.append(msg.value)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/messages")
def messages():
    return jsonify(message_log[-20:])

if __name__ == "__main__":
    t = threading.Thread(target=consume, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5001)
