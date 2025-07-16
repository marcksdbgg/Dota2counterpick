"""
Centralized configuration management using Pydantic Settings.
All environment variables and settings are defined here.
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses Pydantic for validation and type conversion.
    """
    
    # Kafka Configuration
    kafka_bootstrap_servers: str = Field(
        default="localhost:9092",
        description="Kafka bootstrap servers"
    )
    kafka_publish_topic: str = Field(
        default="match_ids_raw",
        description="Kafka topic to publish match IDs"
    )
    
    # OpenDota Stream Configuration
    opendota_stream_url: str = Field(
        default="wss://stream.opendota.com/matches",
        description="OpenDota stream WebSocket URL"
    )
    
    # API Configuration
    api_host: str = Field(
        default="0.0.0.0",
        description="FastAPI host"
    )
    api_port: int = Field(
        default=8000,
        description="FastAPI port"
    )
    
    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    log_format: str = Field(
        default="json",
        description="Log format: json or text"
    )
    
    # Service Configuration
    service_name: str = Field(
        default="ingestion-service",
        description="Service name for logging and metrics"
    )
    
    class Config:
        """Pydantic configuration."""
        env_prefix = ""  # No prefix for environment variables
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
