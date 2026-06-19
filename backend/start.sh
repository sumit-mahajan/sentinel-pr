#!/bin/sh
set -e
uv run python -m worker.main &
exec uv run uvicorn src.api.main:app --host 0.0.0.0 --port "${PORT:-8000}"
