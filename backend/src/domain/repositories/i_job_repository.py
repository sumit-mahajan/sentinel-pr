from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from domain.entities.job import ReviewJob
from domain.value_objects.job_status import JobStatus


class CreateReviewJobParams:
    """Parameters for creating a new review job."""

    def __init__(
        self,
        *,
        repository_id: UUID,
        pr_number: int,
        pr_title: str,
        pr_author: str,
        pr_url: str,
        base_sha: str,
        head_sha: str,
    ) -> None:
        self.repository_id = repository_id
        self.pr_number = pr_number
        self.pr_title = pr_title
        self.pr_author = pr_author
        self.pr_url = pr_url
        self.base_sha = base_sha
        self.head_sha = head_sha


class IJobRepository(ABC):
    @abstractmethod
    async def get_by_repo_and_head_sha(
        self, repository_id: UUID, head_sha: str
    ) -> ReviewJob | None:
        """Return existing job for idempotency check."""

    @abstractmethod
    async def create(self, params: CreateReviewJobParams) -> ReviewJob:
        """Persist a new pending review job."""

    @abstractmethod
    async def get_by_id(self, job_id: UUID) -> ReviewJob | None:
        """Fetch job by primary key."""

    @abstractmethod
    async def update_status(
        self,
        job_id: UUID,
        status: JobStatus,
        *,
        error_message: str | None = None,
    ) -> ReviewJob:
        """Update job lifecycle status."""

    @abstractmethod
    async def update_attempt_count(self, job_id: UUID, attempt_count: int) -> ReviewJob:
        """Increment attempt_count before each execution attempt."""

    @abstractmethod
    async def claim_next_pending(self, max_attempts: int) -> ReviewJob | None:
        """Atomically claim the oldest eligible pending review job."""

    @abstractmethod
    async def release_stale_running(self, stale_minutes: int, max_attempts: int) -> int:
        """Reset crashed running jobs to pending. Returns rows updated."""

    @abstractmethod
    async def schedule_retry(
        self,
        job_id: UUID,
        *,
        retry_after: datetime,
        error_message: str,
    ) -> ReviewJob:
        """Mark job pending with a future retry_after timestamp."""
