#!/bin/sh
set -e
uv run uvicorn worker.http:app --host 0.0.0.0 --port 8001 &
exec uv run uvicorn src.api.main:app --host 0.0.0.0 --port "${PORT:-8000}"
