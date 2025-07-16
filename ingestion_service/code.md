# Plan de Desarrollo: Microservicio de Ingesta (`ingestion-service`)

Este documento detalla el diseño técnico y el plan de desarrollo para el `ingestion-service`. Su propósito es servir como una guía de implementación para los ingenieros de software, asegurando que se sigan las mejores prácticas de arquitectura y diseño.

## 1. Principios y Buenas Prácticas Generales

Antes de detallar el servicio, establecemos las prácticas fundamentales que regirán su desarrollo. La adherencia a estos principios es obligatoria para garantizar la calidad, mantenibilidad y escalabilidad del backend.

### 1.1. Arquitectura Hexagonal (Puertos y Adaptadores)
Esta arquitectura es el pilar de nuestro diseño. Su objetivo es aislar la lógica de negocio central (el "Dominio" y la "Aplicación") de las preocupaciones externas como bases de datos, APIs de terceros, o colas de mensajes (la "Infraestructura").

*   **Núcleo (Core):** Contiene el `Dominio` (entidades y lógica de negocio pura) y la capa de `Aplicación` (casos de uso que orquestan el dominio). **El núcleo no tiene dependencias de ninguna tecnología de infraestructura externa.**
*   **Puertos (Ports):** Son interfaces (clases base abstractas en Python) definidas en la capa de `Aplicación`. Definen los contratos que el núcleo necesita para comunicarse con el mundo exterior (ej. `IMessagePublisher`, `ISourceStreamConsumer`).
*   **Adaptadores (Adapters):** Son las implementaciones concretas de los puertos y se encuentran en la capa de `Infraestructura`. Un `Adaptador de Entrada` (Driving) invoca un caso de uso (ej. un consumidor de Kafka que recibe un mensaje). Un `Adaptador de Salida` (Driven) es invocado por un caso de uso (ej. un publicador de Kafka que envía un mensaje).

**Beneficios Clave:**
*   **Máxima Testeabilidad:** El núcleo puede ser probado en total aislamiento, utilizando "mocks" o "fakes" de los puertos.
*   **Intercambiabilidad Tecnológica:** Podemos cambiar nuestro broker de mensajes de Kafka a RabbitMQ simplemente escribiendo un nuevo adaptador, sin tocar una sola línea del núcleo de la aplicación.
*   **Evolución Enfocada:** El dominio y la lógica de negocio pueden evolucionar sin preocuparse por los detalles de la infraestructura.

### 1.2. Programación Orientada a Objetos (POO) y SOLID
Utilizaremos un enfoque estricto de POO, adhiriéndonos a los principios SOLID para crear un código limpio y mantenible.

*   **Clases y Encapsulación:** Toda la lógica estará encapsulada en clases con responsabilidades bien definidas.
*   **Abstracción:** Los puertos son nuestra principal herramienta de abstracción.
*   **Principio de Responsabilidad Única (SRP):** Cada clase tendrá una única razón para cambiar. Un caso de uso, un adaptador, una entidad de dominio.
*   **Principio Abierto/Cerrado (OCP):** El núcleo de la aplicación está cerrado a modificaciones pero abierto a extensiones a través de nuevos adaptadores.
*   **Inversión de Dependencias (DIP):** Las capas de alto nivel (Aplicación) no dependen de las de bajo nivel (Infraestructura). Ambas dependen de abstracciones (Puertos).

### 1.3. FastAPI para la Capa de Adaptadores
Aunque este servicio es principalmente un worker de fondo, utilizaremos FastAPI para exponer una API mínima.
*   **Endpoints de Observabilidad:** Se implementará un endpoint `/health` esencial para las `liveness probes` y `readiness probes` de Kubernetes.
*   **Validación con Pydantic:** Se aprovechará Pydantic para la validación estricta de la configuración y de los datos de entrada/salida de la API.

### 1.4. Gestión de Configuración y Dependencias
*   **Configuración Centralizada:** Se usará una clase de configuración basada en `pydantic-settings` para cargar todas las variables de entorno (URLs de Kafka, nombres de tópicos, etc.), proveyendo validación y tipos desde el inicio.
*   **Inyección de Dependencias (DI):** Ensamblaremos la aplicación en el punto de entrada (`main.py`), inyectando las dependencias concretas (los adaptadores) en las clases que las necesitan (los casos de uso). Esto desacopla el código y facilita las pruebas.

---

## 2. Plan de Desarrollo Detallado del `ingestion-service`

### 2.1. Objetivo y Responsabilidades
El `ingestion-service` tiene una única responsabilidad: **Actuar como un puente resiliente y de alto rendimiento entre el stream de datos de partidas de OpenDota y nuestra propia plataforma de eventos Kafka.**

**Responsabilidades Clave:**
*   **Consumir** datos del stream público de OpenDota.
*   **Validar y transformar** el dato crudo (ID de la partida) a un modelo de dominio simple.
*   **Publicar** este modelo de dominio en un tópico específico de nuestro clúster de Kafka interno.
*   **No debe** realizar enriquecimiento de datos complejo. Su trabajo es entregar el mensaje de forma rápida y fiable. El enriquecimiento es responsabilidad del `etl-service`.
*   **Ser observable** a través de logs estructurados y un endpoint de salud.

### 2.2. Estructura Detallada de la Codebase

Se adoptará la siguiente estructura de directorios, que refleja fielmente la Arquitectura Hexagonal.

```
ingestion-service/
├── app/
│   ├── __init__.py
│   ├── domain/                         # -- CORE: Lógica de negocio pura (la burbuja interior)
│   │   ├── __init__.py
│   │   ├── models.py                   # Entidades y objetos de valor (ej: Match)
│   │   └── exceptions.py               # Excepciones de dominio personalizadas
│   ├── application/                      # -- CORE: Orquestación (la segunda burbuja)
│   │   ├── __init__.py
│   │   ├── ports/                      # Interfaces (abstracciones)
│   │   │   ├── __init__.py
│   │   │   ├── message_publisher.py    # Puerto de salida para publicar mensajes
│   │   │   └── source_stream_consumer.py # Puerto de entrada para consumir el stream
│   │   └── use_cases/                  # Implementación de los casos de uso
│   │       ├── __init__.py
│   │       └── process_match_stream.py # Caso de uso que conecta los puertos
│   ├── infrastructure/                   # -- EXTERIOR: Implementaciones concretas
│   │   ├── __init__.py
│   │   ├── adapters/
│   │   │   ├── __init__.py
│   │   │   ├── kafka_publisher.py      # Adaptador que implementa IMessagePublisher con Kafka
│   │   │   └── opendota_consumer.py    # Adaptador que implementa ISourceStreamConsumer
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── v1/
│   │       │   └── endpoints/
│   │       │       └── health.py       # Endpoint de salud de FastAPI
│   │       └── server.py               # Configuración de la instancia de FastAPI
│   ├── core/                           # -- Lógica de aplicación transversal
│   │   ├── __init__.py
│   │   ├── config.py                   # Configuración de la aplicación (Pydantic)
│   │   └── logging.py                  # Configuración del logger estructurado
│   └── main.py                         # Punto de entrada: ensambla e inicia la aplicación
├── tests/
│   ├── __init__.py
│   ├── unit/                           # Pruebas unitarias del dominio y aplicación (con mocks)
│   └── integration/                    # Pruebas de los adaptadores contra servicios reales (Docker)
├── pyproject.toml                      # Dependencias y configuración del proyecto (Poetry)
└── Dockerfile                          # Definición de la imagen del contenedor
```

### 2.3. Descripción de Componentes Clave

#### `app/domain`
*   **`models.py`**:
    *   `Match` (Pydantic Model): Define la entidad principal. Inicialmente, podría contener solo `match_id: int`. Se usarán validadores de Pydantic para asegurar que `match_id` sea un entero positivo.
*   **`exceptions.py`**:
    *   `InvalidMatchDataError`: Excepción personalizada que se lanzará si los datos recibidos del stream no cumplen con el formato esperado.

#### `app/application`
*   **`ports/message_publisher.py`**:
    *   `IMessagePublisher` (ABC): Define la interfaz para cualquier publicador de mensajes.
        *   `async def publish(self, topic: str, match: Match) -> None:`: Contrato para publicar un objeto `Match`.
*   **`ports/source_stream_consumer.py`**:
    *   `ISourceStreamConsumer` (ABC): Define la interfaz para cualquier consumidor de streams.
        *   `async def start_consuming(self) -> None:`: Contrato para iniciar el proceso de consumo de forma indefinida.
*   **`use_cases/process_match_stream.py`**:
    *   `ProcessMatchStreamUseCase`: La clase que implementa la lógica central.
        *   `__init__(self, publisher: IMessagePublisher)`: Recibe el publicador a través de inyección de dependencias.
        *   `async def execute(self, raw_data: dict) -> None:`: Este es el corazón. Recibe datos crudos, intenta parsearlos a un `Match` del dominio, y si tiene éxito, usa el `publisher` inyectado para enviar el `Match`. Maneja las `InvalidMatchDataError`.

#### `app/infrastructure`
*   **`adapters/kafka_publisher.py`**:
    *   `KafkaMessagePublisher` (implementa `IMessagePublisher`): Adaptador concreto.
        *   `__init__`: Recibe la configuración de Kafka (brokers, etc.).
        *   `publish`: Contiene la lógica para serializar el `Match` a JSON y publicarlo en el tópico de Kafka especificado, usando la librería `aiokafka`.
*   **`adapters/opendota_consumer.py`**:
    *   `OpenDotaStreamConsumer` (implementa `ISourceStreamConsumer`): Adaptador de entrada.
        *   `__init__`: Recibe la URL del stream de OpenDota y una instancia del `ProcessMatchStreamUseCase`.
        *   `start_consuming`: Implementa el bucle infinito que se conecta al stream (posiblemente usando `aiohttp` para una conexión WebSocket o SSE), recibe los mensajes y, por cada mensaje, invoca `use_case.execute(raw_data)`.
*   **`api/`**:
    *   `server.py`: Crea y configura la instancia de FastAPI.
    *   `endpoints/health.py`: Define un router de FastAPI con una ruta `GET /health` que devuelve un `200 OK` con `{"status": "alive"}`.

#### `app/core`
*   **`config.py`**:
    *   `Settings` (hereda de `pydantic_settings.BaseSettings`): Define y carga desde variables de entorno todas las configuraciones: `KAFKA_BROKER_URL`, `KAFKA_PUBLISH_TOPIC`, `OPENDOTA_STREAM_URL`, etc.
*   **`logging.py`**:
    *   Función `setup_logging`: Configura `structlog` para tener logs en formato JSON, listos para ser consumidos por sistemas de observabilidad como ELK o Grafana Loki.

#### `app/main.py` - El Ensamblador
Este es el único lugar donde las clases concretas de infraestructura se encuentran con las clases del núcleo de la aplicación.
1.  Cargar la configuración desde `core.config`.
2.  Configurar el logging.
3.  Instanciar el adaptador de salida: `publisher = KafkaMessagePublisher(config)`.
4.  Instanciar el caso de uso, inyectando el adaptador: `use_case = ProcessMatchStreamUseCase(publisher)`.
5.  Instanciar el adaptador de entrada, inyectando el caso de uso: `consumer = OpenDotaStreamConsumer(config, use_case)`.
6.  Iniciar la aplicación: Ejecutar `consumer.start_consuming()` y el servidor `uvicorn` para la API de salud, probablemente usando `asyncio.gather`.