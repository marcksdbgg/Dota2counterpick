"""
Caso de uso central para procesar datos del stream de partidas.
Contiene la lógica de negocio para la ingesta y publicación.
"""
import structlog
from typing import Dict, Any

from app.domain.models import Match
from app.domain.exceptions import InvalidMatchDataError, MatchValidationError
from app.application.ports.message_publisher import IMessagePublisher

logger = structlog.get_logger(__name__)

class ProcessMatchStreamUseCase:
    """
    Orquesta la lógica de negocio:
    1. Recibe datos crudos del stream.
    2. Valida y transforma al modelo de dominio.
    3. Publica en el message broker a través de un puerto.
    """

    def __init__(self, publisher: IMessagePublisher, topic: str):
        """
        Inicializa el caso de uso con sus dependencias inyectadas.
        
        Args:
            publisher: Implementación del puerto de publicación.
            topic: Nombre del topic donde publicar las partidas.
        """
        self._publisher = publisher
        self._topic = topic

    async def execute(self, raw_data: Dict[str, Any]) -> None:
        """
        Procesa los datos crudos de una partida recibida del stream.
        
        Args:
            raw_data: Diccionario con los datos crudos.
        """
        try:
            match_id = self._extract_match_id(raw_data)
            match = Match(match_id=match_id)
            
            await self._publisher.publish(self._topic, match)
            
            logger.info(f"Successfully processed match {match.match_id}")

        except (InvalidMatchDataError, MatchValidationError) as e:
            logger.warning("Failed to process match data", reason=str(e), data=e.raw_data if hasattr(e, 'raw_data') else raw_data)
        except Exception as e:
            logger.error("Unexpected error processing match data", error=e, exc_info=True)

    def _extract_match_id(self, raw_data: Dict[str, Any]) -> int:
        """
        Extrae y valida el `match_id` de los datos crudos.
        
        Raises:
            InvalidMatchDataError: Si los datos no son válidos.
        """
        if not isinstance(raw_data, dict):
            raise InvalidMatchDataError("Raw data must be a dictionary", raw_data)
        
        match_id = raw_data.get("match_id")
        
        if match_id is None:
            raise InvalidMatchDataError("Missing 'match_id' field", raw_data)
        
        if not isinstance(match_id, int) or match_id <= 0:
            raise InvalidMatchDataError(f"Invalid match_id: {match_id}. Must be positive integer.", raw_data)
        
        return match_id