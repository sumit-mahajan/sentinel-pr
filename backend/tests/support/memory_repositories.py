from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from domain.entities.embedding_cleanup_job import EmbeddingCleanupJob
from domain.entities.github_installation import GithubInstallation
from domain.entities.job import ReviewJob
from domain.entities.repository import Repository
from domain.errors import EntityNotFoundError
from domain.repositories.i_embedding_cleanup_job_repository import (
    CreateEmbeddingCleanupJobParams,
    IEmbeddingCleanupJobRepository,
)
from domain.repositories.i_embedding_cleanup_repository import IEmbeddingCleanupRepository
from domain.repositories.i_installation_repository import (
    IInstallationRepository,
    UpsertInstallationParams,
)
from domain.repositories.i_job_repository import CreateReviewJobParams, IJobRepository
from domain.repositories.i_repo_repository import IRepoRepository, UpsertRepositoryParams
from domain.value_objects.job_status import JobStatus


class InMemoryRepoRepository(IRepoRepository):
    def __init__(self) -> None:
        self._repos: dict[int, Repository] = {}

    async def get_by_github_id(self, github_id: int) -> Repository | None:
        return self._repos.get(github_id)

    async def get_by_id(self, repository_id: UUID) -> Repository | None:
        for repo in self._repos.values():
            if repo.id == repository_id:
                return repo
        return None

    async def upsert(self, params: UpsertRepositoryParams) -> Repository:
        now = datetime.now(UTC)
        existing = self._repos.get(params.github_id)
        if existing:
            updated = Repository(
                id=existing.id,
                github_id=params.github_id,
                installation_id=params.installation_id,
                owner=params.owner,
                name=params.name,
                full_name=params.full_name,
                default_branch=params.default_branch,
                is_active=existing.is_active,
                language=params.language,
                created_at=existing.created_at,
                updated_at=now,
            )
        else:
            updated = Repository(
                id=uuid4(),
                github_id=params.github_id,
                installation_id=params.installation_id,
                owner=params.owner,
                name=params.name,
                full_name=params.full_name,
                default_branch=params.default_branch,
                is_active=True,
                language=params.language,
                created_at=now,
                updated_at=now,
            )
        self._repos[params.github_id] = updated
        return updated

    async def list_accessible_for_login(self, login: str) -> list[Repository]:
        return [r for r in self._repos.values() if r.owner == login]

    async def update_is_active(self, repository_id: UUID, is_active: bool) -> Repository:
        for key, repo in self._repos.items():
            if repo.id == repository_id:
                updated = Repository(
                    id=repo.id,
                    github_id=repo.github_id,
                    installation_id=repo.installation_id,
                    owner=repo.owner,
                    name=repo.name,
                    full_name=repo.full_name,
                    default_branch=repo.default_branch,
                    is_active=is_active,
                    language=repo.language,
                    created_at=repo.created_at,
                    updated_at=datetime.now(UTC),
                )
                self._repos[key] = updated
                return updated
        raise EntityNotFoundError(f"Repository {repository_id} not found")


class InMemoryJobRepository(IJobRepository):
    def __init__(self) -> None:
        self._jobs: dict[tuple[UUID, str], ReviewJob] = {}

    async def get_by_repo_and_head_sha(
        self, repository_id: UUID, head_sha: str
    ) -> ReviewJob | None:
        return self._jobs.get((repository_id, head_sha))

    async def create(self, params: CreateReviewJobParams) -> ReviewJob:
        now = datetime.now(UTC)
        job = ReviewJob(
            id=uuid4(),
            repository_id=params.repository_id,
            pr_number=params.pr_number,
            pr_title=params.pr_title,
            pr_author=params.pr_author,
            pr_url=params.pr_url,
            base_sha=params.base_sha,
            head_sha=params.head_sha,
            status=JobStatus.PENDING,
            attempt_count=0,
            retry_after=None,
            error_message=None,
            enqueued_at=now,
            started_at=None,
            completed_at=None,
            created_at=now,
            updated_at=now,
        )
        self._jobs[(params.repository_id, params.head_sha)] = job
        return job

    async def get_by_id(self, job_id: UUID) -> ReviewJob | None:
        for job in self._jobs.values():
            if job.id == job_id:
                return job
        return None

    async def update_attempt_count(self, job_id: UUID, attempt_count: int) -> ReviewJob:
        for key, job in self._jobs.items():
            if job.id == job_id:
                updated = ReviewJob(
                    id=job.id,
                    repository_id=job.repository_id,
                    pr_number=job.pr_number,
                    pr_title=job.pr_title,
                    pr_author=job.pr_author,
                    pr_url=job.pr_url,
                    base_sha=job.base_sha,
                    head_sha=job.head_sha,
                    status=job.status,
                    attempt_count=attempt_count,
                    retry_after=job.retry_after,
                    error_message=job.error_message,
                    enqueued_at=job.enqueued_at,
                    started_at=job.started_at,
                    completed_at=job.completed_at,
                    created_at=job.created_at,
                    updated_at=datetime.now(UTC),
                )
                self._jobs[key] = updated
                return updated
        raise EntityNotFoundError(f"Review job {job_id} not found")

    async def update_status(
        self,
        job_id: UUID,
        status: JobStatus,
        *,
        error_message: str | None = None,
    ) -> ReviewJob:
        for key, job in self._jobs.items():
            if job.id == job_id:
                started_at = job.started_at
                completed_at = job.completed_at
                if status == JobStatus.RUNNING and started_at is None:
                    started_at = datetime.now(UTC)
                if status in {JobStatus.COMPLETED, JobStatus.FAILED}:
                    completed_at = datetime.now(UTC)
                updated = ReviewJob(
                    id=job.id,
                    repository_id=job.repository_id,
                    pr_number=job.pr_number,
                    pr_title=job.pr_title,
                    pr_author=job.pr_author,
                    pr_url=job.pr_url,
                    base_sha=job.base_sha,
                    head_sha=job.head_sha,
                    status=status,
                    attempt_count=job.attempt_count,
                    retry_after=job.retry_after,
                    error_message=error_message,
                    enqueued_at=job.enqueued_at,
                    started_at=started_at,
                    completed_at=completed_at,
                    created_at=job.created_at,
                    updated_at=datetime.now(UTC),
                )
                self._jobs[key] = updated
                return updated
        raise EntityNotFoundError(f"Review job {job_id} not found")

    async def claim_next_pending(self, max_attempts: int) -> ReviewJob | None:
        now = datetime.now(UTC)
        eligible = [
            job
            for job in self._jobs.values()
            if job.status == JobStatus.PENDING
            and job.attempt_count < max_attempts
            and (job.retry_after is None or job.retry_after <= now)
        ]
        if not eligible:
            return None
        job = sorted(eligible, key=lambda item: item.enqueued_at)[0]
        return await self.update_status(job.id, JobStatus.RUNNING)

    async def release_stale_running(self, stale_minutes: int, max_attempts: int) -> int:
        cutoff = datetime.now(UTC) - timedelta(minutes=stale_minutes)
        released = 0
        for key, job in list(self._jobs.items()):
            if (
                job.status == JobStatus.RUNNING
                and job.started_at is not None
                and job.started_at < cutoff
                and job.attempt_count < max_attempts
            ):
                self._jobs[key] = ReviewJob(
                    id=job.id,
                    repository_id=job.repository_id,
                    pr_number=job.pr_number,
                    pr_title=job.pr_title,
                    pr_author=job.pr_author,
                    pr_url=job.pr_url,
                    base_sha=job.base_sha,
                    head_sha=job.head_sha,
                    status=JobStatus.PENDING,
                    attempt_count=job.attempt_count,
                    retry_after=job.retry_after,
                    error_message=job.error_message,
                    enqueued_at=job.enqueued_at,
                    started_at=None,
                    completed_at=job.completed_at,
                    created_at=job.created_at,
                    updated_at=datetime.now(UTC),
                )
                released += 1
        return released

    async def schedule_retry(
        self,
        job_id: UUID,
        *,
        retry_after: datetime,
        error_message: str,
    ) -> ReviewJob:
        for key, job in self._jobs.items():
            if job.id == job_id:
                updated = ReviewJob(
                    id=job.id,
                    repository_id=job.repository_id,
                    pr_number=job.pr_number,
                    pr_title=job.pr_title,
                    pr_author=job.pr_author,
                    pr_url=job.pr_url,
                    base_sha=job.base_sha,
                    head_sha=job.head_sha,
                    status=JobStatus.PENDING,
                    attempt_count=job.attempt_count,
                    retry_after=retry_after,
                    error_message=error_message,
                    enqueued_at=job.enqueued_at,
                    started_at=None,
                    completed_at=None,
                    created_at=job.created_at,
                    updated_at=datetime.now(UTC),
                )
                self._jobs[key] = updated
                return updated
        raise EntityNotFoundError(f"Review job {job_id} not found")


class InMemoryInstallationRepository(IInstallationRepository):
    def __init__(self) -> None:
        self._installations: dict[int, GithubInstallation] = {}

    async def get_by_installation_id(self, installation_id: int) -> GithubInstallation | None:
        return self._installations.get(installation_id)

    async def get_by_id(self, installation_uuid: UUID) -> GithubInstallation | None:
        for inst in self._installations.values():
            if inst.id == installation_uuid:
                return inst
        return None

    async def upsert(self, params: UpsertInstallationParams) -> GithubInstallation:
        now = datetime.now(UTC)
        existing = self._installations.get(params.installation_id)
        if existing:
            updated = GithubInstallation(
                id=existing.id,
                installation_id=params.installation_id,
                account_login=params.account_login,
                account_type=params.account_type,
                account_avatar_url=params.account_avatar_url,
                access_token_encrypted=existing.access_token_encrypted,
                access_token_expires_at=existing.access_token_expires_at,
                created_at=existing.created_at,
                updated_at=now,
            )
        else:
            updated = GithubInstallation(
                id=uuid4(),
                installation_id=params.installation_id,
                account_login=params.account_login,
                account_type=params.account_type,
                account_avatar_url=params.account_avatar_url,
                access_token_encrypted=None,
                access_token_expires_at=None,
                created_at=now,
                updated_at=now,
            )
        self._installations[params.installation_id] = updated
        return updated

    async def update_access_token(
        self,
        installation_uuid: UUID,
        *,
        access_token_encrypted: str,
        access_token_expires_at: datetime,
    ) -> GithubInstallation:
        for key, inst in self._installations.items():
            if inst.id == installation_uuid:
                updated = GithubInstallation(
                    id=inst.id,
                    installation_id=inst.installation_id,
                    account_login=inst.account_login,
                    account_type=inst.account_type,
                    account_avatar_url=inst.account_avatar_url,
                    access_token_encrypted=access_token_encrypted,
                    access_token_expires_at=access_token_expires_at,
                    created_at=inst.created_at,
                    updated_at=datetime.now(UTC),
                )
                self._installations[key] = updated
                return updated
        raise EntityNotFoundError(f"Installation {installation_uuid} not found")


class InMemoryEmbeddingCleanupRepository(IEmbeddingCleanupRepository):
    """Tracks deletion calls for unit testing without a real DB."""

    def __init__(self) -> None:
        self.deleted_shas: list[tuple[UUID, str]] = []
        self.stale_calls: list[int] = []

    async def delete_by_repo_and_sha(self, repository_id: UUID, commit_sha: str) -> int:
        self.deleted_shas.append((repository_id, commit_sha))
        return 5  # simulate deleting 5 rows

    async def delete_older_than_days(self, days: int) -> int:
        self.stale_calls.append(days)
        return 10  # simulate deleting 10 stale rows


class InMemoryEmbeddingCleanupJobRepository(IEmbeddingCleanupJobRepository):
    def __init__(self) -> None:
        self._jobs: dict[tuple[UUID, str], EmbeddingCleanupJob] = {}

    async def get_by_repo_and_head_sha(
        self, repository_id: UUID, head_sha: str
    ) -> EmbeddingCleanupJob | None:
        return self._jobs.get((repository_id, head_sha))

    async def create(self, params: CreateEmbeddingCleanupJobParams) -> EmbeddingCleanupJob:
        now = datetime.now(UTC)
        job = EmbeddingCleanupJob(
            id=uuid4(),
            repository_id=params.repository_id,
            head_sha=params.head_sha,
            pr_number=params.pr_number,
            status=JobStatus.PENDING,
            attempt_count=0,
            retry_after=None,
            error_message=None,
            enqueued_at=now,
            started_at=None,
            completed_at=None,
            created_at=now,
            updated_at=now,
        )
        self._jobs[(params.repository_id, params.head_sha)] = job
        return job

    async def get_by_id(self, job_id: UUID) -> EmbeddingCleanupJob | None:
        for job in self._jobs.values():
            if job.id == job_id:
                return job
        return None

    async def claim_next_pending(self, max_attempts: int) -> EmbeddingCleanupJob | None:
        now = datetime.now(UTC)
        eligible = [
            job
            for job in self._jobs.values()
            if job.status == JobStatus.PENDING
            and job.attempt_count < max_attempts
            and (job.retry_after is None or job.retry_after <= now)
        ]
        if not eligible:
            return None
        job = sorted(eligible, key=lambda item: item.enqueued_at)[0]
        return await self.update_status(job.id, JobStatus.RUNNING)

    async def release_stale_running(self, stale_minutes: int, max_attempts: int) -> int:
        return 0

    async def update_attempt_count(self, job_id: UUID, attempt_count: int) -> EmbeddingCleanupJob:
        for key, job in self._jobs.items():
            if job.id == job_id:
                updated = EmbeddingCleanupJob(
                    id=job.id,
                    repository_id=job.repository_id,
                    head_sha=job.head_sha,
                    pr_number=job.pr_number,
                    status=job.status,
                    attempt_count=attempt_count,
                    retry_after=job.retry_after,
                    error_message=job.error_message,
                    enqueued_at=job.enqueued_at,
                    started_at=job.started_at,
                    completed_at=job.completed_at,
                    created_at=job.created_at,
                    updated_at=datetime.now(UTC),
                )
                self._jobs[key] = updated
                return updated
        raise EntityNotFoundError(f"Embedding cleanup job {job_id} not found")

    async def update_status(
        self,
        job_id: UUID,
        status: JobStatus,
        *,
        error_message: str | None = None,
    ) -> EmbeddingCleanupJob:
        for key, job in self._jobs.items():
            if job.id == job_id:
                updated = EmbeddingCleanupJob(
                    id=job.id,
                    repository_id=job.repository_id,
                    head_sha=job.head_sha,
                    pr_number=job.pr_number,
                    status=status,
                    attempt_count=job.attempt_count,
                    retry_after=job.retry_after,
                    error_message=error_message,
                    enqueued_at=job.enqueued_at,
                    started_at=job.started_at,
                    completed_at=job.completed_at,
                    created_at=job.created_at,
                    updated_at=datetime.now(UTC),
                )
                self._jobs[key] = updated
                return updated
        raise EntityNotFoundError(f"Embedding cleanup job {job_id} not found")

    async def schedule_retry(
        self,
        job_id: UUID,
        *,
        retry_after: datetime,
        error_message: str,
    ) -> EmbeddingCleanupJob:
        for key, job in self._jobs.items():
            if job.id == job_id:
                updated = EmbeddingCleanupJob(
                    id=job.id,
                    repository_id=job.repository_id,
                    head_sha=job.head_sha,
                    pr_number=job.pr_number,
                    status=JobStatus.PENDING,
                    attempt_count=job.attempt_count,
                    retry_after=retry_after,
                    error_message=error_message,
                    enqueued_at=job.enqueued_at,
                    started_at=None,
                    completed_at=None,
                    created_at=job.created_at,
                    updated_at=datetime.now(UTC),
                )
                self._jobs[key] = updated
                return updated
        raise EntityNotFoundError(f"Embedding cleanup job {job_id} not found")
