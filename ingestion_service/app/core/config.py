import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "match_ids_raw")
OPENDOTA_STREAM_URL = os.getenv("OPENDOTA_STREAM_URL", "wss://stream.opendota.com/matches")
