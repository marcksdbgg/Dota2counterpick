# Stage 1: Build stage
FROM python:3.12-slim as builder

# Set working directory
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy only dependency configuration files
COPY pyproject.toml poetry.lock* ./

# Install dependencies into a virtual environment
# --no-dev: don't install development dependencies
# --no-interaction: don't ask interactive questions
# --no-ansi: disable ANSI output
RUN poetry install --no-dev --no-interaction --no-ansi


# Stage 2: Final stage
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set non-root user
ARG UID=10001
RUN adduser --system --uid ${UID} appuser

# Copy virtual env from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY ./app ./app

# Set ownership of the app directory
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Make sure scripts in .venv are in PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "None"]