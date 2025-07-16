"""
Unit tests for domain models.
"""
import pytest
from pydantic import ValidationError

from app.domain.models import Match


class TestMatch:
    """Test the Match domain entity."""
    
    def test_create_valid_match(self):
        """Test creating a valid Match entity."""
        # Arrange & Act
        match = Match(match_id=123456)
        
        # Assert
        assert match.match_id == 123456
    
    def test_match_id_must_be_positive(self):
        """Test that match_id must be positive."""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Match(match_id=-1)
        
        assert "match_id must be a positive integer" in str(exc_info.value)
    
    def test_match_id_zero_invalid(self):
        """Test that match_id cannot be zero."""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Match(match_id=0)
        
        assert "match_id must be a positive integer" in str(exc_info.value)
    
    def test_to_dict(self):
        """Test serialization to dictionary."""
        # Arrange
        match = Match(match_id=789)
        
        # Act
        result = match.to_dict()
        
        # Assert
        assert result == {"match_id": 789}
        assert isinstance(result, dict)
