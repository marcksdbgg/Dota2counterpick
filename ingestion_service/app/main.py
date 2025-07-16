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
