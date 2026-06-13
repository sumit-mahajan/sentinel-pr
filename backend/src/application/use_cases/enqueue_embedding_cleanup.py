import structlog

from domain.errors import EntityNotFoundError
from domain.repositories.i_repo_repository import IRepoRepository
from domain.services.i_queue_client import IQueueClient, QueueMessage
from domain.value_objects.job_type import JobType

logger = structlog.get_logger()


class EnqueueEmbeddingCleanupUseCase:
    """Enqueue embedding cleanup when a pull request is closed."""

    def __init__(self, repo_repo: IRepoRepository, queue: IQueueClient) -> None:
        self._repo_repo = repo_repo
        self._queue = queue

    async def execute(
        self,
        *,
        repository_github_id: int,
        head_sha: str,
        pr_number: int,
    ) -> bool:
        repo = await self._repo_repo.get_by_github_id(repository_github_id)
        if repo is None:
            raise EntityNotFoundError(
                f"Repository github_id={repository_github_id} is not registered"
            )

        await self._queue.enqueue(
            QueueMessage(
                job_type=JobType.EMBEDDING_CLEANUP,
                job_id=None,
                repository_id=repo.id,
                head_sha=head_sha,
                pr_number=pr_number,
            )
        )

        log = logger.bind(
            repo=repo.full_name,
            pr_number=pr_number,
            head_sha=head_sha,
        )
        await log.ainfo("embedding_cleanup_enqueued")
        return True
