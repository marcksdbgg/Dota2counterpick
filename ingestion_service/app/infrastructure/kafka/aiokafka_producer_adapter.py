from aiokafka import AIOKafkaProducer
from app.application.ports.kafka_producer_port import KafkaProducerPort
from app.core.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
import json

class AiokafkaProducerAdapter(KafkaProducerPort):
    def __init__(self):
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send(self, match_id: int):
        if not self.producer:
            await self.start()
        await self.producer.send_and_wait(KAFKA_TOPIC, json.dumps({"match_id": match_id}).encode())
