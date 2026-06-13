from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.use_cases.start_review import StartReviewUseCase
from domain.entities.job import ReviewJob
from domain.entities.repository import Repository
from domain.errors import EntityNotFoundError
from domain.repositories.i_job_repository import CreateReviewJobParams
from domain.value_objects.job_status import JobStatus


def _repo(*, is_active: bool = True) -> Repository:
    now = datetime.now(UTC)
    return Repository(
        id=uuid4(),
        github_id=987654321,
        installation_id=uuid4(),
        owner="acme-corp",
        name="backend",
        full_name="acme-corp/backend",
        default_branch="main",
        is_active=is_active,
        language="Python",
        created_at=now,
        updated_at=now,
    )


def _job(repo_id: object, head_sha: str) -> ReviewJob:
    now = datetime.now(UTC)
    return ReviewJob(
        id=uuid4(),
        repository_id=repo_id,  # type: ignore[arg-type]
        pr_number=42,
        pr_title="Fix auth",
        pr_author="john",
        pr_url="https://github.com/acme-corp/backend/pull/42",
        base_sha="a" * 40,
        head_sha=head_sha,
        status=JobStatus.PENDING,
        attempt_count=0,
        error_message=None,
        enqueued_at=now,
        started_at=None,
        completed_at=None,
        created_at=now,
        updated_at=now,
    )


@pytest.mark.asyncio
async def test_start_review_enqueues_new_job() -> None:
    repo = _repo()
    job = _job(repo.id, "b" * 40)

    job_repo = AsyncMock()
    job_repo.get_by_repo_and_head_sha.return_value = None
    job_repo.create.return_value = job

    repo_repo = AsyncMock()
    repo_repo.get_by_github_id.return_value = repo

    queue = AsyncMock()

    use_case = StartReviewUseCase(job_repo, repo_repo, queue)
    result_job, enqueued = await use_case.execute(
        repository_github_id=repo.github_id,
        pr_number=42,
        pr_title="Fix auth",
        pr_author="john",
        pr_url="https://github.com/acme-corp/backend/pull/42",
        base_sha="a" * 40,
        head_sha="b" * 40,
    )

    assert result_job == job
    assert enqueued is True
    job_repo.create.assert_awaited_once()
    queue.enqueue.assert_awaited_once()


@pytest.mark.asyncio
async def test_start_review_skips_duplicate_head_sha() -> None:
    repo = _repo()
    existing = _job(repo.id, "b" * 40)

    job_repo = AsyncMock()
    job_repo.get_by_repo_and_head_sha.return_value = existing

    repo_repo = AsyncMock()
    repo_repo.get_by_github_id.return_value = repo

    queue = AsyncMock()

    use_case = StartReviewUseCase(job_repo, repo_repo, queue)
    result_job, enqueued = await use_case.execute(
        repository_github_id=repo.github_id,
        pr_number=42,
        pr_title="Fix auth",
        pr_author="john",
        pr_url="https://github.com/acme-corp/backend/pull/42",
        base_sha="a" * 40,
        head_sha="b" * 40,
    )

    assert result_job == existing
    assert enqueued is False
    job_repo.create.assert_not_awaited()
    queue.enqueue.assert_not_awaited()


@pytest.mark.asyncio
async def test_start_review_skips_inactive_repo() -> None:
    repo = _repo(is_active=False)

    job_repo = AsyncMock()
    repo_repo = AsyncMock()
    repo_repo.get_by_github_id.return_value = repo
    queue = AsyncMock()

    use_case = StartReviewUseCase(job_repo, repo_repo, queue)
    result_job, enqueued = await use_case.execute(
        repository_github_id=repo.github_id,
        pr_number=42,
        pr_title="Fix auth",
        pr_author="john",
        pr_url="https://github.com/acme-corp/backend/pull/42",
        base_sha="a" * 40,
        head_sha="b" * 40,
    )

    assert result_job is None
    assert enqueued is False


@pytest.mark.asyncio
async def test_start_review_raises_for_unknown_repo() -> None:
    job_repo = AsyncMock()
    repo_repo = AsyncMock()
    repo_repo.get_by_github_id.return_value = None
    queue = AsyncMock()

    use_case = StartReviewUseCase(job_repo, repo_repo, queue)

    with pytest.raises(EntityNotFoundError):
        await use_case.execute(
            repository_github_id=999,
            pr_number=1,
            pr_title="t",
            pr_author="a",
            pr_url="u",
            base_sha="a" * 40,
            head_sha="b" * 40,
        )
