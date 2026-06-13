from uuid import uuid4

import pytest

from application.use_cases.cleanup_embeddings import CleanupEmbeddingsUseCase
from tests.support.memory_repositories import InMemoryEmbeddingCleanupRepository


@pytest.mark.asyncio
async def test_cleanup_for_pr_calls_repo() -> None:
    repo = InMemoryEmbeddingCleanupRepository()
    use_case = CleanupEmbeddingsUseCase(repo)

    repo_id = uuid4()
    deleted = await use_case.cleanup_for_pr(repo_id, "abc123")

    assert deleted == 5
    assert repo.deleted_shas == [(repo_id, "abc123")]


@pytest.mark.asyncio
async def test_cleanup_stale_uses_default_days() -> None:
    repo = InMemoryEmbeddingCleanupRepository()
    use_case = CleanupEmbeddingsUseCase(repo)

    deleted = await use_case.cleanup_stale()
    assert deleted == 10
    assert repo.stale_calls == [30]


@pytest.mark.asyncio
async def test_cleanup_stale_accepts_custom_days() -> None:
    repo = InMemoryEmbeddingCleanupRepository()
    use_case = CleanupEmbeddingsUseCase(repo)

    await use_case.cleanup_stale(days=7)
    assert repo.stale_calls == [7]
