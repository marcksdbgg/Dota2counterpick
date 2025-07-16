"""
Main entry point for the ingestion service.
This is where dependency injection and application assembly occurs.
"""
import asyncio
from contextlib import asynccontextmanager

import uvicorn
import structlog
from fastapi import FastAPI

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.infrastructure.api.server import create_app
from app.infrastructure.kafka.aiokafka_producer_adapter import KafkaMessagePublisher
from app.infrastructure.match_stream.opendota_stream_adapter import OpenDotaStreamConsumer
from app.application.use_cases.ingest_match_ids_use_case import ProcessMatchStreamUseCase

logger = structlog.get_logger(__name__)
consumer_task: asyncio.Task | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager.
    Handles startup and shutdown of background services like the stream consumer.
    """
    global consumer_task
    
    setup_logging(
        log_level=settings.log_level,
        log_format=settings.log_format,
        service_name=settings.service_name
    )
    
    logger.info("Starting ingestion service...")
    
    # 1. Create the driven adapter (output)
    publisher = KafkaMessagePublisher(settings.kafka_bootstrap_servers)
    await publisher.start()
    
    # 2. Create the use case, injecting the adapter
    use_case = ProcessMatchStreamUseCase(
        publisher=publisher,
        topic=settings.kafka_publish_topic
    )
    
    # 3. Create the driving adapter (input), injecting the use case
    consumer = OpenDotaStreamConsumer(
        stream_url=settings.opendota_stream_url,
        use_case=use_case
    )
    
    # 4. Start the consumer in a background task
    consumer_task = asyncio.create_task(consumer.start_consuming())
    
    logger.info("Ingestion service started successfully.")
    
    try:
        yield
    finally:
        logger.info("Shutting down ingestion service...")
        if consumer_task and not consumer_task.done():
            consumer_task.cancel()
            try:
                await consumer_task
            except asyncio.CancelledError:
                logger.info("Consumer task successfully cancelled.")
        
        await consumer.stop_consuming()
        await publisher.stop()
        logger.info("Ingestion service shutdown complete.")


# Create the FastAPI app instance with the lifespan manager
app = create_app()
app.router.lifespan_context = lifespan


def main() -> None:
    """
    Main function to run the Uvicorn server.
    """
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False,
        log_config=None, # We use our custom structlog config
    )

if __name__ == "__main__":
    main()