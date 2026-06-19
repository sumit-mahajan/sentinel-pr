"""Shared constants for DB-backed job polling."""

MAX_JOB_ATTEMPTS = 3

# Seconds before a failed job is eligible for retry (attempt 1 → 2s, 2 → 8s, 3 → terminal)
RETRY_BACKOFF_SECONDS = [2, 8, 32]

STALE_RUNNING_MINUTES = 15

DEFAULT_POLL_INTERVAL_SECONDS = 5.0
