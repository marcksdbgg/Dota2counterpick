"""
Structured logging configuration using structlog.
Provides JSON-formatted logs for observability.
"""
import logging
import sys
import structlog


def setup_logging(
    log_level: str = "INFO",
    log_format: str = "json",
    service_name: str = "ingestion-service"
) -> None:
    """
    Configure structured logging for the entire application.
    This setup redirects standard library logging to be processed by structlog,
    ensuring all logs are consistently formatted.
    """
    log_level_upper = log_level.upper()
    
    # Define processors shared by all logs
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            ]
        ),
    ]

    # Configure structlog itself
    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Choose the final renderer based on log_format
    renderer = (
        structlog.processors.JSONRenderer()
        if log_format == "json"
        else structlog.dev.ConsoleRenderer(colors=True)
    )

    # Configure the formatter for standard library logs
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processor=renderer,
    )

    # Configure the root logger
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level_upper)

    # Add service context to all logs
    structlog.contextvars.bind_contextvars(service=service_name)