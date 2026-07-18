from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json, os, time

app = Flask(__name__)
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")

producer = None

def connect_producer(max_attempts=15, delay_seconds=5):
    global producer
    for attempt in range(1, max_attempts + 1):
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                request_timeout_ms=10000
            )
            print(f"Connected to Kafka on attempt {attempt}", flush=True)
            return
        except Exception as e:
            print(f"Kafka not ready (attempt {attempt}/{max_attempts}): {e}", flush=True)
            time.sleep(delay_seconds)
    raise RuntimeError("Could not connect to Kafka after max attempts")

connect_producer()

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json(force=True)
    producer.send("events", data)
    producer.flush()
    return jsonify({"status": "sent", "data": data})

@app.route("/health")
def health():
    return jsonify({"status": "ok" , "version": "2"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
