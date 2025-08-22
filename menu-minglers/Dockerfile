# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH=/app \
  POETRY_VERSION=1.7.1 \
  POETRY_HOME="/opt/poetry" \
  POETRY_VENV_IN_PROJECT=1 \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="/app/.venv/bin:$PATH"

# Install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  curl \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set work directory
WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.in-project true \
  && poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY app/ ./app/

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
