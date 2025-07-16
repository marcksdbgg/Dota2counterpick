"""
Domain models for the ingestion service.
Contains pure business logic without external dependencies.
"""
from pydantic import BaseModel, Field, field_validator

from app.domain.exceptions import MatchValidationError


class Match(BaseModel):
    """
    Core domain entity representing a Dota 2 match.
    This is the primary entity that flows through our system.
    """
    match_id: int = Field(..., description="Unique identifier for the match")

    @field_validator('match_id')
    @classmethod
    def validate_match_id(cls, v: int) -> int:
        """Validate that the match_id is a positive integer."""
        if v <= 0:
            raise MatchValidationError('match_id must be a positive integer', match_id=v)
        return v

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {"match_id": self.match_id}