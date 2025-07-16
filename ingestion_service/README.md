# ingestion-service

Servicio de ingesta de IDs de partidas de OpenDota y publicación en Kafka.

## Estructura
- Arquitectura hexagonal.
- Python, FastAPI, AIOHTTP, aiokafka.

## Uso
1. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta el servicio:
   ```bash
   uvicorn app.main:app --reload
   ```

## Configuración
Variables de entorno:
- `KAFKA_BOOTSTRAP_SERVERS`
- `KAFKA_TOPIC`
- `OPENDOTA_STREAM_URL`
