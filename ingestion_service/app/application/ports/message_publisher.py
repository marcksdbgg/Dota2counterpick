"""
Port for publishing messages to message brokers.
This is an output port (driven adapter will implement this).
"""
from abc import ABC, abstractmethod
from app.domain.models import Match


class IMessagePublisher(ABC):
    """
    Interface for publishing Match entities to message queues.
    This port defines the contract for message publishing adapters.
    """
    
    @abstractmethod
    async def publish(self, topic: str, match: Match) -> None:
        """
        Publish a Match entity to the specified topic.
        
        Args:
            topic: The topic/queue name to publish to
            match: The Match entity to publish
        """
        pass
    
    @abstractmethod
    async def start(self) -> None:
        """Initialize the publisher connection."""
        pass
    
    @abstractmethod
    async def stop(self) -> None:
        """Cleanup publisher resources."""
        pass
