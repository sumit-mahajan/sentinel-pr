"""Poll Postgres for pending jobs and dispatch them to use cases."""

from __future__ import annotations

import structlog

from domain.value_objects.job_poll import (
    MAX_JOB_ATTEMPTS,
    STALE_RUNNING_MINUTES,
)
from infrastructure.config.settings import Settings
from infrastructure.db.repositories.embedding_cleanup_job_repository import (
    PostgresEmbeddingCleanupJobRepository,
)
from infrastructure.db.repositories.job_repository import PostgresJobRepository
from infrastructure.db.session import create_session_factory
from worker.dispatcher_factory import dispatch_cleanup_job, dispatch_review_job

logger = structlog.get_logger()


async def poll_and_process(settings: Settings) -> int:
    """Claim and process all eligible pending jobs. Returns jobs processed."""
    session_factory = create_session_factory(settings)
    processed = 0

    async with session_factory() as db:
        job_repo = PostgresJobRepository(db)
        cleanup_repo = PostgresEmbeddingCleanupJobRepository(db)

        stale_minutes = settings.worker_stale_running_minutes
        released = await job_repo.release_stale_running(stale_minutes, MAX_JOB_ATTEMPTS)
        released += await cleanup_repo.release_stale_running(stale_minutes, MAX_JOB_ATTEMPTS)
        if released:
            await logger.ainfo("worker_stale_jobs_released", count=released)

    while True:
        async with session_factory() as claim_session:
            job_repo = PostgresJobRepository(claim_session)
            job = await job_repo.claim_next_pending(MAX_JOB_ATTEMPTS)
            if job is None:
                break
            job_id = job.id

        await dispatch_review_job(settings, job_id)
        processed += 1

    while True:
        async with session_factory() as claim_session:
            cleanup_repo = PostgresEmbeddingCleanupJobRepository(claim_session)
            cleanup_job = await cleanup_repo.claim_next_pending(MAX_JOB_ATTEMPTS)
            if cleanup_job is None:
                break
            cleanup_job_id = cleanup_job.id

        await dispatch_cleanup_job(settings, cleanup_job_id)
        processed += 1

    if processed:
        await logger.ainfo("worker_poll_complete", processed=processed)

    return processed
