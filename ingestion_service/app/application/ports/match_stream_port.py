from abc import ABC, abstractmethod

class MatchStreamPort(ABC):
    @abstractmethod
    async def listen(self):
        pass
