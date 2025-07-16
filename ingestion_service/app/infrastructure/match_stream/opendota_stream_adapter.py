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
