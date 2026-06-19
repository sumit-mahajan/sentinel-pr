from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.use_cases.enqueue_embedding_cleanup import EnqueueEmbeddingCleanupUseCase
from domain.entities.repository import Repository
from domain.errors import EntityNotFoundError
from tests.support.memory_repositories import InMemoryEmbeddingCleanupJobRepository


def _repo() -> Repository:
    now = datetime.now(UTC)
    return Repository(
        id=uuid4(),
        github_id=987654321,
        installation_id=uuid4(),
        owner="acme-corp",
        name="backend",
        full_name="acme-corp/backend",
        default_branch="main",
        is_active=True,
        language="Python",
        created_at=now,
        updated_at=now,
    )


@pytest.mark.asyncio
async def test_enqueue_embedding_cleanup_success() -> None:
    repo = _repo()
    repo_repo = AsyncMock()
    repo_repo.get_by_github_id.return_value = repo
    cleanup_job_repo = InMemoryEmbeddingCleanupJobRepository()

    use_case = EnqueueEmbeddingCleanupUseCase(repo_repo, cleanup_job_repo)
    result = await use_case.execute(
        repository_github_id=repo.github_id,
        head_sha="c" * 40,
        pr_number=42,
    )

    assert result is True
    stored = await cleanup_job_repo.get_by_repo_and_head_sha(repo.id, "c" * 40)
    assert stored is not None
    assert stored.pr_number == 42


@pytest.mark.asyncio
async def test_enqueue_embedding_cleanup_unknown_repo() -> None:
    repo_repo = AsyncMock()
    repo_repo.get_by_github_id.return_value = None
    cleanup_job_repo = InMemoryEmbeddingCleanupJobRepository()

    use_case = EnqueueEmbeddingCleanupUseCase(repo_repo, cleanup_job_repo)

    with pytest.raises(EntityNotFoundError):
        await use_case.execute(
            repository_github_id=999,
            head_sha="c" * 40,
            pr_number=1,
        )
