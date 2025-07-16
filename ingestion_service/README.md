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
