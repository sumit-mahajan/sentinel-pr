"""
Worker process — consumes review_jobs Redis stream and dispatches jobs.

Run via: python -m worker.main
         docker-compose: command override (see docker-compose.yml)
"""
import asyncio
import json
import signal
import sys

import structlog

from application.use_cases.cleanup_embeddings import CleanupEmbeddingsUseCase
from application.use_cases.run_review_pipeline import RunReviewPipelineUseCase
from infrastructure.ai.stub_orchestrator import StubAgentOrchestrator
from infrastructure.config.settings import get_settings
from infrastructure.db.repositories.job_repository import PostgresJobRepository
from infrastructure.db.session import create_session_factory
from infrastructure.worker.dispatcher import WorkerDispatcher

logger = structlog.get_logger()

POLL_INTERVAL = 5  # seconds between empty-queue polls
BLOCK_MS = 5000    # Redis XREAD block timeout (ms) — 0 = forever


async def _make_dispatcher(settings: object) -> WorkerDispatcher:
    from infrastructure.config.settings import Settings
    assert isinstance(settings, Settings)

    session_factory = create_session_factory(settings)
    orchestrator = StubAgentOrchestrator()  # replaced by real pipeline in F-02

    # Embedding cleanup needs a real DB session.
    # We build a session per-job inside the dispatcher via closure.
    # For now use a single long-lived session (replaced in F-07 with proper scoping).
    session = session_factory()

    async with session as db:
        job_repo = PostgresJobRepository(db)
        run_review = RunReviewPipelineUseCase(job_repo, orchestrator)

        # Embedding cleanup repo wired in F-03/F-07; stub here.
        from tests.support.memory_repositories import InMemoryEmbeddingCleanupRepository  # noqa: PLC0415
        cleanup_use_case = CleanupEmbeddingsUseCase(InMemoryEmbeddingCleanupRepository())

        return WorkerDispatcher(run_review, cleanup_use_case)


async def run_worker() -> None:
    settings = get_settings()

    await logger.ainfo("worker_starting", environment=settings.environment)

    # Resolve queue client
    if settings.upstash_redis_url and settings.upstash_redis_token:
        from upstash_redis import Redis
        redis = Redis(url=settings.upstash_redis_url, token=settings.upstash_redis_token)
        use_redis = True
    else:
        redis = None
        use_redis = False
        await logger.awarning("worker_redis_not_configured_polling_disabled")

    stream = settings.redis_queue_stream
    consumer_group = "workers"
    consumer_name = "worker-1"

    if use_redis and redis is not None:
        try:
            redis.xgroup_create(stream, consumer_group, id="0", mkstream=True)
        except Exception:  # noqa: BLE001
            pass  # Group already exists

    shutdown = asyncio.Event()

    def _handle_signal(*_: object) -> None:
        shutdown.set()

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    await logger.ainfo("worker_ready", stream=stream)

    while not shutdown.is_set():
        if not use_redis or redis is None:
            await asyncio.sleep(POLL_INTERVAL)
            continue

        try:
            entries = redis.xreadgroup(
                consumer_group,
                consumer_name,
                {stream: ">"},
                count=1,
                block=BLOCK_MS,
            )
        except Exception as exc:  # noqa: BLE001
            await logger.aerror("worker_redis_read_error", error=str(exc))
            await asyncio.sleep(POLL_INTERVAL)
            continue

        if not entries:
            continue

        for _stream_name, messages in entries:
            for msg_id, fields in messages:
                raw = fields.get("payload") or fields.get(b"payload") or "{}"
                if isinstance(raw, bytes):
                    raw = raw.decode()

                # Build a fresh dispatcher per message so DB sessions are scoped correctly.
                dispatcher = await _make_dispatcher(settings)

                try:
                    acked = await dispatcher.dispatch(str(raw))
                except Exception as exc:  # noqa: BLE001
                    await logger.aerror("worker_dispatch_error", error=str(exc), msg_id=str(msg_id))
                    acked = False

                if acked:
                    redis.xack(stream, consumer_group, msg_id)

    await logger.ainfo("worker_stopped")


def main() -> None:
    asyncio.run(run_worker())


if __name__ == "__main__":
    main()
