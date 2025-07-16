"""
Unit tests for the ProcessMatchStreamUseCase.
These tests demonstrate the testability of hexagonal architecture.
"""
import pytest
from unittest.mock import AsyncMock, Mock

from app.domain.models import Match
from app.domain.exceptions import InvalidMatchDataError
from app.application.use_cases.ingest_match_ids_use_case import ProcessMatchStreamUseCase
from app.application.ports.message_publisher import IMessagePublisher


class MockMessagePublisher(IMessagePublisher):
    """Mock implementation of message publisher for testing."""
    
    def __init__(self):
        self.published_messages = []
        self.start_called = False
        self.stop_called = False
    
    async def publish(self, topic: str, match: Match) -> None:
        self.published_messages.append((topic, match))
    
    async def start(self) -> None:
        self.start_called = True
    
    async def stop(self) -> None:
        self.stop_called = True


class TestProcessMatchStreamUseCase:
    """Test the core use case logic in isolation."""
    
    @pytest.fixture
    def mock_publisher(self):
        return MockMessagePublisher()
    
    @pytest.fixture
    def use_case(self, mock_publisher):
        return ProcessMatchStreamUseCase(mock_publisher, "test_topic")
    
    @pytest.mark.asyncio
    async def test_execute_with_valid_data(self, use_case, mock_publisher):
        """Test successful processing of valid match data."""
        # Arrange
        raw_data = {"match_id": 123456}
        
        # Act
        await use_case.execute(raw_data)
        
        # Assert
        assert len(mock_publisher.published_messages) == 1
        topic, match = mock_publisher.published_messages[0]
        assert topic == "test_topic"
        assert match.match_id == 123456
    
    @pytest.mark.asyncio
    async def test_execute_with_missing_match_id(self, use_case, mock_publisher):
        """Test handling of data without match_id."""
        # Arrange
        raw_data = {"other_field": "value"}
        
        # Act
        await use_case.execute(raw_data)
        
        # Assert - should not publish anything for invalid data
        assert len(mock_publisher.published_messages) == 0
    
    @pytest.mark.asyncio
    async def test_execute_with_invalid_match_id(self, use_case, mock_publisher):
        """Test handling of invalid match_id values."""
        # Arrange
        raw_data = {"match_id": -1}  # Negative match_id
        
        # Act
        await use_case.execute(raw_data)
        
        # Assert
        assert len(mock_publisher.published_messages) == 0
    
    @pytest.mark.asyncio
    async def test_execute_with_non_dict_data(self, use_case, mock_publisher):
        """Test handling of non-dictionary data."""
        # Arrange
        raw_data = "not a dict"
        
        # Act
        await use_case.execute(raw_data)
        
        # Assert
        assert len(mock_publisher.published_messages) == 0
    
    def test_extract_match_id_valid(self, use_case):
        """Test successful match_id extraction."""
        # Arrange
        raw_data = {"match_id": 999999}
        
        # Act
        result = use_case._extract_match_id(raw_data)
        
        # Assert
        assert result == 999999
    
    def test_extract_match_id_missing_field(self, use_case):
        """Test extraction with missing match_id field."""
        # Arrange
        raw_data = {"other_field": "value"}
        
        # Act & Assert
        with pytest.raises(InvalidMatchDataError) as exc_info:
            use_case._extract_match_id(raw_data)
        
        assert "Missing 'match_id' field" in str(exc_info.value)
    
    def test_extract_match_id_invalid_type(self, use_case):
        """Test extraction with non-integer match_id."""
        # Arrange
        raw_data = {"match_id": "not_an_int"}
        
        # Act & Assert
        with pytest.raises(InvalidMatchDataError) as exc_info:
            use_case._extract_match_id(raw_data)
        
        assert "Invalid match_id" in str(exc_info.value)
