FROM python:3.12-slim

# Install system deps for tree-sitter (C extensions) and asyncpg
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy dependency files first (layer-cache friendly)
COPY pyproject.toml ./
# Copy lockfile if it exists (optional but faster)
COPY uv.lock* ./

# Install production dependencies only
RUN uv sync --frozen --no-dev

# Copy application source
COPY src/ ./src/
COPY worker/ ./worker/

# Non-root user for security
RUN useradd -m -u 1001 appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# Default: API server. Override CMD for worker.
CMD ["uv", "run", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
