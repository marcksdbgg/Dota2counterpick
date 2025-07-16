import aiohttp
from app.application.ports.match_stream_port import MatchStreamPort
from app.core.config import OPENDOTA_STREAM_URL

class OpenDotaStreamAdapter(MatchStreamPort):
    async def listen(self):
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(OPENDOTA_STREAM_URL) as ws:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        # Suponiendo que el mensaje es un JSON con 'match_id'
                        data = msg.json()
                        yield data["match_id"]
