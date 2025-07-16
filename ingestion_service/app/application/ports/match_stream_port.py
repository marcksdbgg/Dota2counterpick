"""
Puerto para consumir datos de partidas desde streams externos.
Este es un puerto de entrada (driving port), un adaptador implementará esta interfaz.
"""
from abc import ABC, abstractmethod

class ISourceStreamConsumer(ABC):
    """
    Define el contrato para los adaptadores que escuchan a streams externos.
    """

    @abstractmethod
    async def start_consuming(self) -> None:
        """
        Inicia el consumo del stream de forma indefinida.
        El método debe gestionar la conexión, reconexión y procesamiento de mensajes.
        """
        pass

    @abstractmethod
    async def stop_consuming(self) -> None:
        """Detiene el consumo del stream de forma controlada."""
        pass