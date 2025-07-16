# Estructura de la Codebase

```
app/
├── .env.example
├── Dockerfile
├── README.md
├── app
│   ├── __init__.py
│   ├── application
│   │   ├── __init__.py
│   │   ├── ports
│   │   │   ├── __init__.py
│   │   │   ├── match_stream_port.py
│   │   │   └── message_publisher.py
│   │   └── use_cases
│   │       ├── __init__.py
│   │       └── ingest_match_ids_use_case.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logging_config.py
│   ├── domain
│   │   ├── __init__.py
│   │   ├── exceptions.py
│   │   └── models.py
│   ├── infrastructure
│   │   ├── __init__.py
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── server.py
│   │   │   └── v1
│   │   │       ├── __init__.py
│   │   │       └── endpoints
│   │   │           ├── __init__.py
│   │   │           └── health.py
│   │   ├── kafka
│   │   │   ├── __init__.py
│   │   │   └── aiokafka_producer_adapter.py
│   │   └── match_stream
│   │       ├── __init__.py
│   │       └── opendota_stream_adapter.py
│   ├── main.py
│   └── utils
│       └── __init__.py
├── export_codebase.py
├── pyproject.toml
└── tests
    ├── __init__.py
    ├── integration
    │   └── __init__.py
    └── unit
        ├── __init__.py
        ├── test_domain_models.py
        └── test_process_match_stream_use_case.py
```

# Codebase: `app`

## File: `.env.example`
```example
# Environment configuration for ingestion-service
# Copy this file to .env and modify the values as needed

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_PUBLISH_TOPIC=match_ids_raw

# OpenDota Stream Configuration
OPENDOTA_STREAM_URL=wss://stream.opendota.com/matches

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json

# Service Configuration
SERVICE_NAME=ingestion-service
```

## File: `app\__init__.py`
```py

```

## File: `app\application\__init__.py`
```py

```

## File: `app\application\ports\__init__.py`
```py

```

## File: `app\application\ports\match_stream_port.py`
```py
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
```

## File: `app\application\ports\message_publisher.py`
```py
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
```

## File: `app\application\use_cases\__init__.py`
```py

```

## File: `app\application\use_cases\ingest_match_ids_use_case.py`
```py
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
```

## File: `app\core\__init__.py`
```py

```

## File: `app\core\config.py`
```py
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

```

## File: `app\core\logging_config.py`
```py
"""
Structured logging configuration using structlog.
Provides JSON-formatted logs for observability.
"""
import logging
import structlog
from typing import Any, Dict
import sys


def setup_logging(
    log_level: str = "INFO",
    log_format: str = "json",
    service_name: str = "ingestion-service"
) -> None:
    """
    Configure structured logging for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_format: Format type (json or text)
        service_name: Service name to include in logs
    """
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper())
    )
    
    # Configure processors based on format
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        # Add service context
        lambda logger, method_name, event_dict: {
            **event_dict,
            "service": service_name
        }
    ]
    
    if log_format == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)

```

## File: `app\domain\__init__.py`
```py

```

## File: `app\domain\exceptions.py`
```py
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

```

## File: `app\domain\models.py`
```py
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

```

## File: `app\infrastructure\__init__.py`
```py

```

## File: `app\infrastructure\api\__init__.py`
```py

```

## File: `app\infrastructure\api\server.py`
```py
"""
FastAPI server configuration for the ingestion service.
This configures the FastAPI instance with proper middleware and routing.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.api.v1.endpoints.health import router as health_router
from app.core.config import settings


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="Ingestion Service",
        description="Dota 2 match data ingestion service",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health_router, prefix="/api/v1")
    
    return app

```

## File: `app\infrastructure\api\v1\__init__.py`
```py

```

## File: `app\infrastructure\api\v1\endpoints\__init__.py`
```py

```

## File: `app\infrastructure\api\v1\endpoints\health.py`
```py
"""
Health endpoint for the ingestion service.
Provides observability for Kubernetes probes.
"""
from fastapi import APIRouter, status
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    service: str


router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    tags=["health"],
    summary="Health Check",
    description="Returns service health status for liveness and readiness probes"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint for Kubernetes probes.
    
    Returns:
        HealthResponse: Service status information
    """
    return HealthResponse(
        status="healthy",
        service="ingestion-service"
    )

```

## File: `app\infrastructure\kafka\__init__.py`
```py

```

## File: `app\infrastructure\kafka\aiokafka_producer_adapter.py`
```py
"""
Kafka adapter implementing the IMessagePublisher port.
This is a driven adapter (infrastructure layer).
"""
import json
import logging
from typing import Optional

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError

from app.application.ports.message_publisher import IMessagePublisher
from app.domain.models import Match


logger = logging.getLogger(__name__)


class KafkaMessagePublisher(IMessagePublisher):
    """
    Kafka implementation of the message publisher port.
    Handles all Kafka-specific concerns while implementing the domain interface.
    """
    
    def __init__(self, bootstrap_servers: str):
        """
        Initialize Kafka publisher.
        
        Args:
            bootstrap_servers: Kafka bootstrap servers string
        """
        self._bootstrap_servers = bootstrap_servers
        self._producer: Optional[AIOKafkaProducer] = None
        self._is_started = False
    
    async def start(self) -> None:
        """Initialize Kafka producer connection."""
        if self._is_started:
            return
            
        try:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self._bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                # Configuration for reliability
                acks='all',  # Wait for all replicas
                # Performance configuration
                compression_type='gzip',
                batch_size=16384,
                linger_ms=10
            )
            
            await self._producer.start()
            self._is_started = True
            logger.info("Kafka producer started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start Kafka producer: {e}")
            raise
    
    async def stop(self) -> None:
        """Cleanup Kafka producer resources."""
        if self._producer and self._is_started:
            try:
                await self._producer.stop()
                self._is_started = False
                logger.info("Kafka producer stopped successfully")
            except Exception as e:
                logger.error(f"Error stopping Kafka producer: {e}")
    
    async def publish(self, topic: str, match: Match) -> None:
        """
        Publish a Match entity to Kafka topic.
        
        Args:
            topic: Kafka topic name
            match: Match domain entity to publish
            
        Raises:
            RuntimeError: If producer is not started
            KafkaError: On Kafka-specific errors
        """
        if not self._is_started or not self._producer:
            raise RuntimeError("Publisher not started. Call start() first.")
        
        try:
            # Convert domain entity to dictionary for serialization
            message_data = match.to_dict()
            
            # Send to Kafka with the match_id as key for partitioning
            await self._producer.send_and_wait(
                topic=topic,
                value=message_data,
                key=str(match.match_id)
            )
            
            logger.debug(f"Published match {match.match_id} to topic {topic}")
            
        except KafkaError as e:
            logger.error(f"Kafka error publishing match {match.match_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error publishing match {match.match_id}: {e}")
            raise

```

## File: `app\infrastructure\match_stream\__init__.py`
```py

```

## File: `app\infrastructure\match_stream\opendota_stream_adapter.py`
```py
"""
OpenDota stream adapter implementing the ISourceStreamConsumer port.
This is a driving adapter (infrastructure layer).
"""
import asyncio
import json
import logging
from typing import Dict, Any

import aiohttp
from aiohttp import WSMsgType

from app.application.ports.match_stream_port import ISourceStreamConsumer
from app.application.use_cases.ingest_match_ids_use_case import ProcessMatchStreamUseCase


logger = logging.getLogger(__name__)


class OpenDotaStreamConsumer(ISourceStreamConsumer):
    """
    OpenDota WebSocket stream consumer.
    Connects to OpenDota's real-time match stream and processes incoming data.
    """
    
    def __init__(self, stream_url: str, use_case: ProcessMatchStreamUseCase):
        """
        Initialize OpenDota stream consumer.
        
        Args:
            stream_url: OpenDota stream WebSocket URL
            use_case: Use case to process received data
        """
        self._stream_url = stream_url
        self._use_case = use_case
        self._running = False
    
    async def start_consuming(self) -> None:
        """
        Start consuming from OpenDota stream indefinitely.
        This method runs forever, reconnecting on failures.
        """
        self._running = True
        logger.info(f"Starting OpenDota stream consumer: {self._stream_url}")
        
        while self._running:
            try:
                await self._connect_and_consume()
            except Exception as e:
                logger.error(f"Stream connection failed: {e}")
                logger.info("Reconnecting in 5 seconds...")
                await asyncio.sleep(5)
    
    async def stop_consuming(self) -> None:
        """Stop the consumer gracefully."""
        self._running = False
        logger.info("OpenDota stream consumer stopped")
    
    async def _connect_and_consume(self) -> None:
        """
        Establish WebSocket connection and consume messages.
        """
        timeout = aiohttp.ClientTimeout(total=None)  # No timeout for WebSocket
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            logger.info(f"Connecting to OpenDota stream: {self._stream_url}")
            
            async with session.ws_connect(
                self._stream_url,
                heartbeat=30,  # Send ping every 30 seconds
                timeout=10     # Connection timeout
            ) as ws:
                logger.info("Successfully connected to OpenDota stream")
                
                async for msg in ws:
                    if not self._running:
                        break
                        
                    await self._process_message(msg)
    
    async def _process_message(self, msg: aiohttp.WSMessage) -> None:
        """
        Process a single WebSocket message.
        
        Args:
            msg: WebSocket message from OpenDota
        """
        try:
            if msg.type == WSMsgType.TEXT:
                # Parse JSON message
                raw_data = json.loads(msg.data)
                
                # Process through use case
                await self._use_case.execute(raw_data)
                
            elif msg.type == WSMsgType.ERROR:
                logger.error(f"WebSocket error: {msg.data}")
                
            elif msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED):
                logger.warning("WebSocket connection closed")
                raise ConnectionError("WebSocket connection closed")
                
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON message: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            # Continue processing other messages

```

## File: `app\main.py`
```py
"""
Main entry point for the ingestion service.
This is where dependency injection and application assembly occurs.
"""
import asyncio
import signal
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.infrastructure.api.server import create_app
from app.infrastructure.kafka.aiokafka_producer_adapter import KafkaMessagePublisher
from app.infrastructure.match_stream.opendota_stream_adapter import OpenDotaStreamConsumer
from app.application.use_cases.ingest_match_ids_use_case import ProcessMatchStreamUseCase


# Global references for cleanup
publisher: KafkaMessagePublisher = None
consumer: OpenDotaStreamConsumer = None
consumer_task: asyncio.Task = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager.
    Handles startup and shutdown of the ingestion service.
    """
    global publisher, consumer, consumer_task
    
    # Setup logging
    setup_logging(
        log_level=settings.log_level,
        log_format=settings.log_format,
        service_name=settings.service_name
    )
    
    import structlog
    logger = structlog.get_logger(__name__)
    
    try:
        # Startup: Assemble and start the application
        logger.info("Starting ingestion service", service=settings.service_name)
        
        # 1. Create and start the message publisher (driven adapter)
        publisher = KafkaMessagePublisher(settings.kafka_bootstrap_servers)
        await publisher.start()
        
        # 2. Create the use case with injected dependencies
        use_case = ProcessMatchStreamUseCase(
            publisher=publisher,
            topic=settings.kafka_publish_topic
        )
        
        # 3. Create the stream consumer (driving adapter) with injected use case
        consumer = OpenDotaStreamConsumer(
            stream_url=settings.opendota_stream_url,
            use_case=use_case
        )
        
        # 4. Start the consumer in a background task
        consumer_task = asyncio.create_task(consumer.start_consuming())
        
        logger.info("Ingestion service started successfully")
        
        yield  # Application runs here
        
    except Exception as e:
        logger.error("Failed to start ingestion service", error=str(e))
        raise
    finally:
        # Shutdown: Clean up resources
        logger.info("Shutting down ingestion service")
        
        if consumer:
            await consumer.stop_consuming()
        
        if consumer_task and not consumer_task.done():
            consumer_task.cancel()
            try:
                await consumer_task
            except asyncio.CancelledError:
                pass
        
        if publisher:
            await publisher.stop()
        
        logger.info("Ingestion service shutdown complete")


def create_application() -> FastAPI:
    """
    Create the FastAPI application with the ingestion service lifespan.
    """
    # Create the FastAPI app with our lifespan manager
    app = create_app()
    app.router.lifespan_context = lifespan
    
    return app


# Create the application instance
app = create_application()


def main() -> None:
    """
    Main entry point when running the service directly.
    """
    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        print(f"\nReceived signal {signum}. Shutting down gracefully...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the server
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False,  # Set to True for development
        log_config=None  # We handle logging ourselves
    )


if __name__ == "__main__":
    main()

```

## File: `app\utils\__init__.py`
```py

```

## File: `Dockerfile`
```
# Dockerfile for ingestion-service
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for some python libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and poetry.lock* first for better layer caching
COPY pyproject.toml poetry.lock* ./

# Install poetry
RUN pip install poetry

# Configure poetry to not create virtualenvs
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY ./app ./app

# Create non-root user for security
RUN adduser --system --group appuser
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Start the application using the lifespan protocol for graceful startup/shutdown
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "None"]
```

## File: `export_codebase.py`
```py
from pathlib import Path

# Carpetas que queremos excluir dentro de /app
EXCLUDED_DIRS = {'.git', '__pycache__', '.venv', '.idea', '.mypy_cache', '.vscode', '.github', 'node_modules'}

def build_tree(directory: Path, prefix: str = "") -> list:
    """
    Genera una representación en árbol de la estructura de directorios y archivos,
    excluyendo las carpetas especificadas en EXCLUDED_DIRS.
    """
    # Filtrar y ordenar los elementos del directorio
    entries = sorted(
        [entry for entry in directory.iterdir() if entry.name not in EXCLUDED_DIRS],
        key=lambda e: e.name
    )
    tree_lines = []
    for index, entry in enumerate(entries):
        connector = "└── " if index == len(entries) - 1 else "├── "
        tree_lines.append(prefix + connector + entry.name)
        if entry.is_dir():
            extension = "    " if index == len(entries) - 1 else "│   "
            tree_lines.extend(build_tree(entry, prefix + extension))
    return tree_lines

def generate_codebase_markdown(base_path: str = ".", output_file: str = "full_codebase.md"):
    base = Path(base_path).resolve()
    app_dir = base

    if not app_dir.exists():
        print(f"[ERROR] La carpeta 'app' no existe en {base}")
        return

    lines = []

    # Agregar la estructura de directorios al inicio del Markdown
    lines.append("# Estructura de la Codebase")
    lines.append("")
    lines.append("```")
    lines.append("app/")
    tree_lines = build_tree(app_dir)
    lines.extend(tree_lines)
    lines.append("```")
    lines.append("")

    # Agregar el contenido de la codebase en Markdown
    lines.append("# Codebase: `app`")
    lines.append("")

    # Recorrer solo la carpeta app
    for path in sorted(app_dir.rglob("*")):
        # Ignorar directorios excluidos
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue

        if path.is_file():
            rel_path = path.relative_to(base)
            lines.append(f"## File: `{rel_path}`")
            try:
                content = path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                lines.append("_[Skipped: binary or non-UTF8 file]_")
                continue
            except Exception as e:
                lines.append(f"_[Error al leer el archivo: {e}]_")
                continue
            ext = path.suffix.lstrip('.')
            lang = ext if ext else ""
            lines.append(f"```{lang}")
            lines.append(content)
            lines.append("```")
            lines.append("")

    # Agregar pyproject.toml si existe en la raíz
    toml_path = base / "pyproject.toml"
    if toml_path.exists():
        lines.append("## File: `pyproject.toml`")
        try:
            content = toml_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            lines.append("_[Skipped: binary or non-UTF8 file]_")
        except Exception as e:
            lines.append(f"_[Error al leer el archivo: {e}]_")
        else:
            lines.append("```toml")
            lines.append(content)
            lines.append("```")
            lines.append("")

    output_path = base / output_file
    try:
        output_path.write_text("\n".join(lines), encoding='utf-8')
        print(f"[OK] Código exportado a Markdown en: {output_path}")
    except Exception as e:
        print(f"[ERROR] Error al escribir el archivo de salida: {e}")

# Si se corre el script directamente
if __name__ == "__main__":
    generate_codebase_markdown()

```

## File: `pyproject.toml`
```toml
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
name = "ingestion-service"
version = "1.0.0"
description = "Dota 2 match data ingestion service"
authors = ["Your Team <team@example.com>"]
readme = "README.md"
packages = [{include = "app"}]

[tool.poetry.dependencies]
python = "^3.12"
fastapi = "^0.104.0"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
aiohttp = "^3.9.0"
aiokafka = "^0.10.0"
pydantic = "^2.5.0"
pydantic-settings = "^2.1.0"
structlog = "^23.2.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
pytest-cov = "^4.1.0"
black = "^23.9.0"
isort = "^5.12.0"
flake8 = "^6.1.0"
mypy = "^1.6.0"

[tool.poetry.scripts]
start = "app.main:main"

[tool.black]
line-length = 88
target-version = ['py312']
include = '\.pyi?$'

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=app --cov-report=term-missing"
asyncio_mode = "auto"

```

## File: `README.md`
```md
# Ingestion Service

Microservicio de ingesta de IDs de partidas de OpenDota siguiendo arquitectura hexagonal.

## Descripción

El `ingestion-service` es un microservicio diseñado para actuar como un puente resiliente y de alto rendimiento entre el stream de datos de partidas de OpenDota y nuestra plataforma de eventos Kafka. Su única responsabilidad es capturar IDs de partidas en tiempo real y publicarlos en un tópico de Kafka.

## Arquitectura

### Hexagonal (Puertos y Adaptadores)

```
┌─────────────────────────────────────────────────────────────────┐
│                        Infrastructure                           │
│  ┌─────────────────┐                    ┌─────────────────┐    │
│  │   OpenDota      │                    │     Kafka       │    │
│  │   Adapter       │                    │    Adapter      │    │
│  │   (Driving)     │                    │   (Driven)      │    │
│  └─────────────────┘                    └─────────────────┘    │
│           │                                       ▲             │
│           │              Application              │             │
│           │  ┌─────────────────────────────────┐  │             │
│           ▼  │                                 │  │             │
│              │    ProcessMatchStreamUseCase    │──┘             │
│              │                                 │                │
│              └─────────────────────────────────┘                │
│                             │                                   │
│                             │        Domain                     │
│                             │  ┌─────────────────┐             │
│                             ▼  │                 │             │
│                                │      Match      │             │
│                                │   (Entity)      │             │
│                                │                 │             │
│                                └─────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

### Responsabilidades

- **Consumir** datos del stream público de OpenDota
- **Validar y transformar** el dato crudo (ID de la partida) a un modelo de dominio
- **Publicar** este modelo en un tópico específico de Kafka
- **Ser observable** a través de logs estructurados y endpoint de salud

## Instalación

### Con Poetry (Recomendado)

```bash
# Instalar Poetry si no lo tienes
curl -sSL https://install.python-poetry.org | python3 -

# Instalar dependencias
poetry install

# Activar entorno virtual
poetry shell
```

### Con pip

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Configuración

1. Copia el archivo de configuración de ejemplo:
```bash
cp .env.example .env
```

2. Edita el archivo `.env` con tu configuración:
```bash
# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_PUBLISH_TOPIC=match_ids_raw

# OpenDota Stream Configuration
OPENDOTA_STREAM_URL=wss://stream.opendota.com/matches

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## Uso

### Desarrollo

```bash
# Con Poetry
poetry run python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Con pip
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# O usando el script principal
python app/main.py
```

### Producción

```bash
# Con Poetry
poetry run python app/main.py

# Con pip
python app/main.py
```

### Docker

```bash
# Construir imagen
docker build -t ingestion-service .

# Ejecutar contenedor
docker run -p 8000:8000 \
  -e KAFKA_BOOTSTRAP_SERVERS=localhost:9092 \
  -e KAFKA_PUBLISH_TOPIC=match_ids_raw \
  ingestion-service
```

## API Endpoints

### Health Check
- **GET** `/api/v1/health` - Endpoint de salud para probes de Kubernetes

```bash
curl http://localhost:8000/api/v1/health
```

### Documentación
- **GET** `/docs` - Swagger UI
- **GET** `/redoc` - ReDoc

## Pruebas

```bash
# Con Poetry
poetry run pytest

# Con pip
pytest

# Con cobertura
pytest --cov=app --cov-report=html
```

## Estructura del Proyecto

```
ingestion-service/
├── app/
│   ├── domain/                    # Lógica de negocio pura
│   │   ├── models.py             # Entidades de dominio
│   │   └── exceptions.py         # Excepciones de dominio
│   ├── application/              # Casos de uso y puertos
│   │   ├── ports/               # Interfaces (abstracciones)
│   │   │   ├── message_publisher.py
│   │   │   └── match_stream_port.py
│   │   └── use_cases/          # Lógica de aplicación
│   │       └── ingest_match_ids_use_case.py
│   ├── infrastructure/          # Adaptadores e infraestructura
│   │   ├── adapters/
│   │   │   ├── kafka_publisher.py
│   │   │   └── opendota_consumer.py
│   │   └── api/               # API REST
│   │       ├── server.py
│   │       └── v1/endpoints/health.py
│   ├── core/                   # Configuración transversal
│   │   ├── config.py          # Configuración de la aplicación
│   │   └── logging_config.py  # Configuración de logging
│   └── main.py               # Punto de entrada
├── tests/
│   ├── unit/                 # Pruebas unitarias
│   └── integration/          # Pruebas de integración
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Observabilidad

### Logs

El servicio utiliza logging estructurado con `structlog`:

```json
{
  "event": "Successfully processed match",
  "match_id": 123456,
  "level": "info",
  "timestamp": "2024-01-15T10:30:00Z",
  "service": "ingestion-service"
}
```

### Métricas

El endpoint `/api/v1/health` puede ser usado para:
- Liveness probes de Kubernetes
- Readiness probes de Kubernetes
- Monitoring externo

## Desarrollo

### Principios Seguidos

1. **Arquitectura Hexagonal**: Separación clara entre dominio, aplicación e infraestructura
2. **SOLID**: Principios de responsabilidad única, abierto/cerrado, inversión de dependencias
3. **Inyección de Dependencias**: Ensamblaje en `main.py`
4. **Configuración Centralizada**: Variables de entorno con Pydantic Settings
5. **Logging Estructurado**: JSON logs para observabilidad

### Agregar Nuevas Funcionalidades

Para agregar un nuevo adaptador de entrada:
1. Implementa la interfaz `ISourceStreamConsumer`
2. Inyecta el `ProcessMatchStreamUseCase` en el constructor
3. Registra en `main.py`

Para agregar un nuevo adaptador de salida:
1. Implementa la interfaz `IMessagePublisher`
2. Inyecta en `ProcessMatchStreamUseCase`
3. Registra en `main.py`

## Dependencias Principales

- **FastAPI**: Framework web asíncrono
- **aiohttp**: Cliente HTTP asíncrono para WebSockets
- **aiokafka**: Cliente Kafka asíncrono
- **Pydantic**: Validación de datos y configuración
- **structlog**: Logging estructurado

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

```

## File: `tests\__init__.py`
```py

```

## File: `tests\integration\__init__.py`
```py

```

## File: `tests\unit\__init__.py`
```py

```

## File: `tests\unit\test_domain_models.py`
```py
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

```

## File: `tests\unit\test_process_match_stream_use_case.py`
```py
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

```

## File: `pyproject.toml`
```toml
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
name = "ingestion-service"
version = "1.0.0"
description = "Dota 2 match data ingestion service"
authors = ["Your Team <team@example.com>"]
readme = "README.md"
packages = [{include = "app"}]

[tool.poetry.dependencies]
python = "^3.12"
fastapi = "^0.104.0"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
aiohttp = "^3.9.0"
aiokafka = "^0.10.0"
pydantic = "^2.5.0"
pydantic-settings = "^2.1.0"
structlog = "^23.2.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
pytest-cov = "^4.1.0"
black = "^23.9.0"
isort = "^5.12.0"
flake8 = "^6.1.0"
mypy = "^1.6.0"

[tool.poetry.scripts]
start = "app.main:main"

[tool.black]
line-length = 88
target-version = ['py312']
include = '\.pyi?$'

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=app --cov-report=term-missing"
asyncio_mode = "auto"

```
