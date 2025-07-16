"""
Core use case for processing match stream data.
This contains the business logic for ingesting and publishing match data.
"""
import logging
from typing import Dict, Any

from app.domain.models import Match
from app.domain.exceptions import InvalidMatchDataError, MatchValidationError
from app.application.ports.message_publisher import IMessagePublisher


logger = logging.getLogger(__name__)


class ProcessMatchStreamUseCase:
    """
    Use case that orchestrates the core business logic:
    1. Receive raw data from stream
    2. Validate and transform to domain model
    3. Publish to message broker
    """
    
    def __init__(self, publisher: IMessagePublisher, topic: str):
        """
        Initialize use case with injected dependencies.
        
        Args:
            publisher: Message publisher implementation
            topic: Topic name to publish matches to
        """
        self._publisher = publisher
        self._topic = topic
        
    async def execute(self, raw_data: Dict[str, Any]) -> None:
        """
        Process raw match data from the stream.
        
        Args:
            raw_data: Raw data received from external stream
            
        Raises:
            InvalidMatchDataError: When data doesn't contain valid match info
            MatchValidationError: When match fails domain validation
        """
        try:
            # Extract match_id from raw data
            match_id = self._extract_match_id(raw_data)
            
            # Create domain entity
            match = Match(match_id=match_id)
            
            # Publish to message broker
            await self._publisher.publish(self._topic, match)
            
            logger.info(f"Successfully processed match {match_id}")
            
        except (InvalidMatchDataError, MatchValidationError) as e:
            logger.warning(f"Failed to process match data: {e}")
            # In this service, we log and continue - don't let individual
            # bad messages stop the entire stream processing
        except Exception as e:
            logger.error(f"Unexpected error processing match data: {e}")
            # For unexpected errors, we also continue but log as error
    
    def _extract_match_id(self, raw_data: Dict[str, Any]) -> int:
        """
        Extract and validate match_id from raw stream data.
        
        Args:
            raw_data: Raw data from stream
            
        Returns:
            Valid match ID
            
        Raises:
            InvalidMatchDataError: When match_id is missing or invalid
        """
        if not isinstance(raw_data, dict):
            raise InvalidMatchDataError(
                "Raw data must be a dictionary", 
                raw_data
            )
        
        match_id = raw_data.get("match_id")
        
        if match_id is None:
            raise InvalidMatchDataError(
                "Missing 'match_id' field in raw data", 
                raw_data
            )
        
        if not isinstance(match_id, int) or match_id <= 0:
            raise InvalidMatchDataError(
                f"Invalid match_id: {match_id}. Must be positive integer", 
                raw_data
            )
        
        return match_id
