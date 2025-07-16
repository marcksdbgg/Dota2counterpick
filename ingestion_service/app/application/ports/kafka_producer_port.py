from abc import ABC, abstractmethod

class KafkaProducerPort(ABC):
    @abstractmethod
    async def send(self, match_id: int):
        pass
