import structlog

from domain.entities.job import ReviewJob
from domain.errors import EntityNotFoundError
from domain.repositories.i_job_repository import CreateReviewJobParams, IJobRepository
from domain.repositories.i_repo_repository import IRepoRepository
from domain.services.i_queue_client import IQueueClient, QueueMessage
from domain.value_objects.job_status import JobStatus
from domain.value_objects.job_type import JobType

logger = structlog.get_logger()


class StartReviewUseCase:
    """Enqueue a review job for a pull request event."""

    def __init__(
        self,
        job_repo: IJobRepository,
        repo_repo: IRepoRepository,
        queue: IQueueClient,
    ) -> None:
        self._job_repo = job_repo
        self._repo_repo = repo_repo
        self._queue = queue

    async def execute(
        self,
        *,
        repository_github_id: int,
        pr_number: int,
        pr_title: str,
        pr_author: str,
        pr_url: str,
        base_sha: str,
        head_sha: str,
    ) -> tuple[ReviewJob | None, bool]:
        """
        Create review job and enqueue to Redis.

        Returns (job, enqueued) where enqueued=False when idempotent skip applies.
        """
        repo = await self._repo_repo.get_by_github_id(repository_github_id)
        if repo is None:
            raise EntityNotFoundError(
                f"Repository github_id={repository_github_id} is not registered"
            )

        if not repo.is_active:
            log = logger.bind(repo=repo.full_name, pr_number=pr_number, head_sha=head_sha)
            await log.ainfo("review_skipped_inactive_repo")
            return None, False

        existing = await self._job_repo.get_by_repo_and_head_sha(repo.id, head_sha)
        if existing is not None:
            log = logger.bind(
                job_id=str(existing.id),
                repo=repo.full_name,
                pr_number=pr_number,
                head_sha=head_sha,
            )
            await log.ainfo("review_job_idempotent_skip", status=existing.status.value)
            return existing, False

        job = await self._job_repo.create(
            CreateReviewJobParams(
                repository_id=repo.id,
                pr_number=pr_number,
                pr_title=pr_title,
                pr_author=pr_author,
                pr_url=pr_url,
                base_sha=base_sha,
                head_sha=head_sha,
            )
        )

        await self._queue.enqueue(
            QueueMessage(
                job_type=JobType.REVIEW,
                job_id=job.id,
                repository_id=repo.id,
                head_sha=head_sha,
                pr_number=pr_number,
            )
        )

        log = logger.bind(
            job_id=str(job.id),
            repo=repo.full_name,
            pr_number=pr_number,
            head_sha=head_sha,
        )
        await log.ainfo("review_job_enqueued")

        return job, True
