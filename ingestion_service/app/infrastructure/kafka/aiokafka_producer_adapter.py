"""
Kafka adapter implementing the IMessagePublisher port.
This is a driven adapter (infrastructure layer).
"""
import json
import logging
from typing import Optional

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError

from app.application.ports.message_publisher import IMessagePublisher
from app.domain.models import Match


logger = logging.getLogger(__name__)


class KafkaMessagePublisher(IMessagePublisher):
    """
    Kafka implementation of the message publisher port.
    Handles all Kafka-specific concerns while implementing the domain interface.
    """
    
    def __init__(self, bootstrap_servers: str):
        """
        Initialize Kafka publisher.
        
        Args:
            bootstrap_servers: Kafka bootstrap servers string
        """
        self._bootstrap_servers = bootstrap_servers
        self._producer: Optional[AIOKafkaProducer] = None
        self._is_started = False
    
    async def start(self) -> None:
        """Initialize Kafka producer connection."""
        if self._is_started:
            return
            
        try:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self._bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                # Configuration for reliability
                acks='all',  # Wait for all replicas
                # Performance configuration
                compression_type='gzip',
                batch_size=16384,
                linger_ms=10
            )
            
            await self._producer.start()
            self._is_started = True
            logger.info("Kafka producer started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start Kafka producer: {e}")
            raise
    
    async def stop(self) -> None:
        """Cleanup Kafka producer resources."""
        if self._producer and self._is_started:
            try:
                await self._producer.stop()
                self._is_started = False
                logger.info("Kafka producer stopped successfully")
            except Exception as e:
                logger.error(f"Error stopping Kafka producer: {e}")
    
    async def publish(self, topic: str, match: Match) -> None:
        """
        Publish a Match entity to Kafka topic.
        
        Args:
            topic: Kafka topic name
            match: Match domain entity to publish
            
        Raises:
            RuntimeError: If producer is not started
            KafkaError: On Kafka-specific errors
        """
        if not self._is_started or not self._producer:
            raise RuntimeError("Publisher not started. Call start() first.")
        
        try:
            # Convert domain entity to dictionary for serialization
            message_data = match.to_dict()
            
            # Send to Kafka with the match_id as key for partitioning
            await self._producer.send_and_wait(
                topic=topic,
                value=message_data,
                key=str(match.match_id)
            )
            
            logger.debug(f"Published match {match.match_id} to topic {topic}")
            
        except KafkaError as e:
            logger.error(f"Kafka error publishing match {match.match_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error publishing match {match.match_id}: {e}")
            raise
