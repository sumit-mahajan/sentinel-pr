from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from domain.entities.embedding_cleanup_job import EmbeddingCleanupJob
from domain.value_objects.job_status import JobStatus


class CreateEmbeddingCleanupJobParams:
    def __init__(
        self,
        *,
        repository_id: UUID,
        head_sha: str,
        pr_number: int,
    ) -> None:
        self.repository_id = repository_id
        self.head_sha = head_sha
        self.pr_number = pr_number


class IEmbeddingCleanupJobRepository(ABC):
    @abstractmethod
    async def get_by_repo_and_head_sha(
        self, repository_id: UUID, head_sha: str
    ) -> EmbeddingCleanupJob | None:
        """Return existing cleanup job for idempotency."""

    @abstractmethod
    async def create(self, params: CreateEmbeddingCleanupJobParams) -> EmbeddingCleanupJob:
        """Persist a new pending cleanup job."""

    @abstractmethod
    async def get_by_id(self, job_id: UUID) -> EmbeddingCleanupJob | None:
        """Fetch cleanup job by primary key."""

    @abstractmethod
    async def claim_next_pending(self, max_attempts: int) -> EmbeddingCleanupJob | None:
        """Atomically claim the oldest eligible pending job."""

    @abstractmethod
    async def release_stale_running(self, stale_minutes: int, max_attempts: int) -> int:
        """Reset crashed running jobs to pending. Returns rows updated."""

    @abstractmethod
    async def update_attempt_count(self, job_id: UUID, attempt_count: int) -> EmbeddingCleanupJob:
        """Set attempt_count before each execution attempt."""

    @abstractmethod
    async def update_status(
        self,
        job_id: UUID,
        status: JobStatus,
        *,
        error_message: str | None = None,
    ) -> EmbeddingCleanupJob:
        """Update job lifecycle status."""

    @abstractmethod
    async def schedule_retry(
        self,
        job_id: UUID,
        *,
        retry_after: datetime,
        error_message: str,
    ) -> EmbeddingCleanupJob:
        """Mark job pending with a future retry_after timestamp."""
