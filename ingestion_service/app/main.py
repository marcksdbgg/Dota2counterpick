import asyncio
from fastapi import FastAPI
from app.api.v1.endpoints import ingestion_endpoint
from app.infrastructure.match_stream.opendota_stream_adapter import OpenDotaStreamAdapter
from app.infrastructure.kafka.aiokafka_producer_adapter import AiokafkaProducerAdapter
from app.application.use_cases.ingest_match_ids_use_case import IngestMatchIDsUseCase
import logging

app = FastAPI()
app.include_router(ingestion_endpoint.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    logging.info("Starting ingestion service...")
    match_stream = OpenDotaStreamAdapter()
    kafka_producer = AiokafkaProducerAdapter()
    use_case = IngestMatchIDsUseCase(match_stream, kafka_producer)
    asyncio.create_task(use_case.run())
