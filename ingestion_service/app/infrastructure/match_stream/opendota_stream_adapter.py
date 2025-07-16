"""
OpenDota stream adapter implementing the ISourceStreamConsumer port.
This is a driving adapter (infrastructure layer).
"""
import asyncio
import json
import structlog
import aiohttp
from aiohttp import WSMsgType

from app.application.ports.match_stream_port import ISourceStreamConsumer
from app.application.use_cases.ingest_match_ids_use_case import ProcessMatchStreamUseCase

logger = structlog.get_logger(__name__)

class OpenDotaStreamConsumer(ISourceStreamConsumer):
    """
    OpenDota WebSocket stream consumer.
    Connects to OpenDota's real-time match stream and processes incoming data.
    """
    
    def __init__(self, stream_url: str, use_case: ProcessMatchStreamUseCase):
        self._stream_url = stream_url
        self._use_case = use_case
        self._running = False
    
    async def start_consuming(self) -> None:
        """
        Start consuming from OpenDota stream indefinitely.
        This method runs forever, reconnecting on failures.
        """
        self._running = True
        logger.info("Starting OpenDota stream consumer", url=self._stream_url)
        
        while self._running:
            try:
                await self._connect_and_consume()
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                logger.warning("Stream connection failed, reconnecting in 5s...", error=str(e))
                await asyncio.sleep(5)
            except Exception as e:
                logger.error("Unexpected stream consumer error, reconnecting in 15s...", error=str(e), exc_info=True)
                await asyncio.sleep(15)

    async def stop_consuming(self) -> None:
        """Stop the consumer gracefully."""
        self._running = False
        logger.info("Stopping OpenDota stream consumer.")
    
    async def _connect_and_consume(self) -> None:
        """
        Establish WebSocket connection and consume messages.
        """
        timeout = aiohttp.ClientTimeout(total=None, connect=10, sock_connect=10)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.ws_connect(self._stream_url, heartbeat=30) as ws:
                logger.info("Successfully connected to OpenDota stream.")
                
                async for msg in ws:
                    if not self._running:
                        break
                    await self._process_message(msg)

                logger.info("Exited message consumption loop.")

    async def _process_message(self, msg: aiohttp.WSMessage) -> None:
        """
        Process a single WebSocket message.
        """
        if msg.type == WSMsgType.TEXT:
            try:
                raw_data = json.loads(msg.data)
                await self._use_case.execute(raw_data)
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON message", data=msg.data)
        elif msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED):
            raise aiohttp.ClientError(f"WebSocket connection closed by server. Close code: {ws.close_code}")
        elif msg.type == WSMsgType.ERROR:
            logger.error("WebSocket error received", error=msg.data)
            raise aiohttp.ClientError(f"WebSocket error: {msg.data}")