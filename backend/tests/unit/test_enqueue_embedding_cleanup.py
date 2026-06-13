from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.use_cases.enqueue_embedding_cleanup import EnqueueEmbeddingCleanupUseCase
from domain.entities.repository import Repository
from domain.errors import EntityNotFoundError
from domain.value_objects.job_type import JobType


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
    queue = AsyncMock()

    use_case = EnqueueEmbeddingCleanupUseCase(repo_repo, queue)
    result = await use_case.execute(
        repository_github_id=repo.github_id,
        head_sha="c" * 40,
        pr_number=42,
    )

    assert result is True
    queue.enqueue.assert_awaited_once()
    message = queue.enqueue.await_args.args[0]
    assert message.job_type == JobType.EMBEDDING_CLEANUP
    assert message.head_sha == "c" * 40


@pytest.mark.asyncio
async def test_enqueue_embedding_cleanup_unknown_repo() -> None:
    repo_repo = AsyncMock()
    repo_repo.get_by_github_id.return_value = None
    queue = AsyncMock()

    use_case = EnqueueEmbeddingCleanupUseCase(repo_repo, queue)

    with pytest.raises(EntityNotFoundError):
        await use_case.execute(
            repository_github_id=999,
            head_sha="c" * 40,
            pr_number=1,
        )
