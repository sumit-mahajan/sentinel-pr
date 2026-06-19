from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.embedding_cleanup_job import EmbeddingCleanupJob
from domain.errors import EntityNotFoundError
from domain.repositories.i_embedding_cleanup_job_repository import (
    CreateEmbeddingCleanupJobParams,
    IEmbeddingCleanupJobRepository,
)
from domain.value_objects.job_status import JobStatus
from infrastructure.db.models.embedding_cleanup_job import EmbeddingCleanupJobORM
from infrastructure.db.repositories.job_poll_helpers import (
    claim_next_pending_job,
    release_stale_running_jobs,
)
from infrastructure.db.repositories.mappers import to_embedding_cleanup_job_entity


class PostgresEmbeddingCleanupJobRepository(IEmbeddingCleanupJobRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_repo_and_head_sha(
        self, repository_id: UUID, head_sha: str
    ) -> EmbeddingCleanupJob | None:
        result = await self._session.execute(
            select(EmbeddingCleanupJobORM).where(
                EmbeddingCleanupJobORM.repository_id == repository_id,
                EmbeddingCleanupJobORM.head_sha == head_sha,
            )
        )
        orm = result.scalar_one_or_none()
        return to_embedding_cleanup_job_entity(orm) if orm else None

    async def create(self, params: CreateEmbeddingCleanupJobParams) -> EmbeddingCleanupJob:
        now = datetime.now(UTC)
        orm = EmbeddingCleanupJobORM(
            repository_id=params.repository_id,
            head_sha=params.head_sha,
            pr_number=params.pr_number,
            status=JobStatus.PENDING.value,
            attempt_count=0,
            enqueued_at=now,
        )
        self._session.add(orm)
        await self._session.commit()
        await self._session.refresh(orm)
        return to_embedding_cleanup_job_entity(orm)

    async def get_by_id(self, job_id: UUID) -> EmbeddingCleanupJob | None:
        orm = await self._session.get(EmbeddingCleanupJobORM, job_id)
        return to_embedding_cleanup_job_entity(orm) if orm else None

    async def claim_next_pending(self, max_attempts: int) -> EmbeddingCleanupJob | None:
        orm = await claim_next_pending_job(
            self._session, EmbeddingCleanupJobORM, max_attempts=max_attempts
        )
        return to_embedding_cleanup_job_entity(orm) if orm is not None else None  # type: ignore[arg-type]

    async def release_stale_running(self, stale_minutes: int, max_attempts: int) -> int:
        return await release_stale_running_jobs(
            self._session,
            EmbeddingCleanupJobORM,
            stale_minutes=stale_minutes,
            max_attempts=max_attempts,
        )

    async def update_attempt_count(self, job_id: UUID, attempt_count: int) -> EmbeddingCleanupJob:
        orm = await self._session.get(EmbeddingCleanupJobORM, job_id)
        if orm is None:
            raise EntityNotFoundError(f"Embedding cleanup job {job_id} not found")
        orm.attempt_count = attempt_count
        await self._session.commit()
        await self._session.refresh(orm)
        return to_embedding_cleanup_job_entity(orm)

    async def update_status(
        self,
        job_id: UUID,
        status: JobStatus,
        *,
        error_message: str | None = None,
    ) -> EmbeddingCleanupJob:
        orm = await self._session.get(EmbeddingCleanupJobORM, job_id)
        if orm is None:
            raise EntityNotFoundError(f"Embedding cleanup job {job_id} not found")

        orm.status = status.value
        orm.error_message = error_message
        if status == JobStatus.RUNNING and orm.started_at is None:
            orm.started_at = datetime.now(UTC)
        if status in {JobStatus.COMPLETED, JobStatus.FAILED}:
            orm.completed_at = datetime.now(UTC)

        await self._session.commit()
        await self._session.refresh(orm)
        return to_embedding_cleanup_job_entity(orm)

    async def schedule_retry(
        self,
        job_id: UUID,
        *,
        retry_after: datetime,
        error_message: str,
    ) -> EmbeddingCleanupJob:
        orm = await self._session.get(EmbeddingCleanupJobORM, job_id)
        if orm is None:
            raise EntityNotFoundError(f"Embedding cleanup job {job_id} not found")
        orm.status = JobStatus.PENDING.value
        orm.retry_after = retry_after
        orm.error_message = error_message
        orm.started_at = None
        orm.completed_at = None
        await self._session.commit()
        await self._session.refresh(orm)
        return to_embedding_cleanup_job_entity(orm)
