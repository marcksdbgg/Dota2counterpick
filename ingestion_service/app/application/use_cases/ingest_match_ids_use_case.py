class IngestMatchIDsUseCase:
    def __init__(self, match_stream, kafka_producer):
        self.match_stream = match_stream
        self.kafka_producer = kafka_producer

    async def run(self):
        async for match_id in self.match_stream.listen():
            await self.kafka_producer.send(match_id)
