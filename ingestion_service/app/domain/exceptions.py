"""
Domain-specific exceptions for the ingestion service.
These exceptions represent business rule violations.
"""


class DomainException(Exception):
    """Base exception for all domain-related errors."""
    pass


class InvalidMatchDataError(DomainException):
    """
    Raised when received data doesn't conform to expected Match format.
    This is a business rule violation - we only process valid match data.
    """
    def __init__(self, message: str, raw_data: dict = None):
        super().__init__(message)
        self.raw_data = raw_data


class MatchValidationError(DomainException):
    """
    Raised when a Match object fails validation rules.
    """
    def __init__(self, message: str, match_id: int = None):
        super().__init__(message)
        self.match_id = match_id
