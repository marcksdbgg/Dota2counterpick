"""
Domain models for the ingestion service.
Contains pure business logic without external dependencies.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional


class Match(BaseModel):
    """
    Core domain entity representing a Dota 2 match.
    This is the primary entity that flows through our system.
    """
    match_id: int = Field(..., description="Unique identifier for the match")
    
    @validator('match_id')
    def validate_match_id(cls, v):
        if v <= 0:
            raise ValueError('match_id must be a positive integer')
        return v
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {"match_id": self.match_id}
