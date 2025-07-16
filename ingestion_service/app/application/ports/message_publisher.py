"""
Puerto para publicar mensajes a un broker.
Este es un puerto de salida (driven port), un adaptador implementará esta interfaz.
"""
from abc import ABC, abstractmethod
from app.domain.models import Match

class IMessagePublisher(ABC):
    """
    Define el contrato para los adaptadores que publican mensajes.
    """

    @abstractmethod
    async def publish(self, topic: str, match: Match) -> None:
        """
        Publica una entidad Match en el topic especificado.
        
        Args:
            topic: El nombre del topic/cola.
            match: La entidad Match a publicar.
        """
        pass

    @abstractmethod
    async def start(self) -> None:
        """Inicializa el publicador (ej. conexión)."""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Libera los recursos del publicador (ej. cierra conexión)."""
        pass