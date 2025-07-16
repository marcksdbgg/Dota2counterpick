"""
Port for consuming match data from external streams.
This is an input port (driving adapter will implement this).
"""
from abc import ABC, abstractmethod
from typing import AsyncIterator


class ISourceStreamConsumer(ABC):
    """
    Interface for consuming match data from external streaming sources.
    This port defines the contract for adapters that listen to external streams.
    """
    
    @abstractmethod
    async def start_consuming(self) -> None:
        """
        Start consuming the stream indefinitely.
        This method should run forever, processing incoming data.
        """
        pass
