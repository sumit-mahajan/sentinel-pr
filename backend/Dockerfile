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

# Install production dependencies (no lockfile in repo — omit --frozen)
RUN uv sync --no-dev

# Copy application source
COPY src/ ./src/
COPY worker/ ./worker/
COPY start.sh ./start.sh

# Non-root user for security
RUN chmod +x start.sh && useradd -m -u 1001 appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# Default: API server. Override CMD for worker.
CMD ["uv", "run", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
