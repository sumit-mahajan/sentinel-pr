import structlog

from domain.errors import EntityNotFoundError
from domain.repositories.i_embedding_cleanup_job_repository import (
    CreateEmbeddingCleanupJobParams,
    IEmbeddingCleanupJobRepository,
)
from domain.repositories.i_repo_repository import IRepoRepository

logger = structlog.get_logger()


class EnqueueEmbeddingCleanupUseCase:
    """Persist embedding cleanup job when a pull request is closed."""

    def __init__(
        self,
        repo_repo: IRepoRepository,
        cleanup_job_repo: IEmbeddingCleanupJobRepository,
    ) -> None:
        self._repo_repo = repo_repo
        self._cleanup_job_repo = cleanup_job_repo

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

        existing = await self._cleanup_job_repo.get_by_repo_and_head_sha(repo.id, head_sha)
        if existing is not None:
            log = logger.bind(
                repo=repo.full_name,
                pr_number=pr_number,
                head_sha=head_sha,
                job_id=str(existing.id),
            )
            await log.ainfo("embedding_cleanup_idempotent_skip", status=existing.status.value)
            return False

        await self._cleanup_job_repo.create(
            CreateEmbeddingCleanupJobParams(
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
