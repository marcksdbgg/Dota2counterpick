"""
Kafka adapter implementing the IMessagePublisher port.
This is a driven adapter (infrastructure layer).
"""
import json
import structlog
from typing import Optional

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError

from app.application.ports.message_publisher import IMessagePublisher
from app.domain.models import Match

logger = structlog.get_logger(__name__)


class KafkaMessagePublisher(IMessagePublisher):
    """
    Kafka implementation of the message publisher port.
    Handles all Kafka-specific concerns while implementing the domain interface.
    """
    
    def __init__(self, bootstrap_servers: str):
        self._bootstrap_servers = bootstrap_servers
        self._producer: Optional[AIOKafkaProducer] = None
    
    async def start(self) -> None:
        """Initialize Kafka producer connection."""
        if self._producer:
            logger.info("Kafka producer is already started.")
            return
            
        try:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self._bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: str(k).encode('utf-8'),
                acks='all',
                compression_type='gzip',
                batch_size=16384, # 16KB
                linger_ms=10, # Wait 10ms to allow batch to fill
                retry_backoff_ms=100,
            )
            await self._producer.start()
            logger.info("Kafka producer started successfully.")
        except Exception as e:
            logger.error("Failed to start Kafka producer", error=str(e), exc_info=True)
            raise
    
    async def stop(self) -> None:
        """Cleanup Kafka producer resources."""
        if self._producer:
            logger.info("Stopping Kafka producer...")
            try:
                await self._producer.stop()
                self._producer = None
                logger.info("Kafka producer stopped successfully.")
            except Exception as e:
                logger.error("Error stopping Kafka producer", error=str(e), exc_info=True)
    
    async def publish(self, topic: str, match: Match) -> None:
        """
        Publish a Match entity to Kafka topic.
        """
        if not self._producer:
            raise RuntimeError("Publisher not started. Call start() first.")
        
        try:
            message_data = match.to_dict()
            await self._producer.send_and_wait(
                topic=topic,
                value=message_data,
                key=match.match_id  # Use match_id as key for partitioning
            )
            logger.debug("Published match to Kafka", match_id=match.match_id, topic=topic)
        except KafkaError as e:
            logger.error("Kafka error publishing match", match_id=match.match_id, error=str(e), exc_info=True)
            raise