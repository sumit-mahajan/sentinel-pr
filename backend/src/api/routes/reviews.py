from uuid import UUID

from fastapi import APIRouter, Query

from api.middleware.auth_middleware import CurrentUser, DbSession
from api.schemas.dashboard import JobStatusDTO, PaginatedResponse, ReviewDetailDTO
from application.use_cases.get_job import GetJobUseCase
from application.use_cases.list_reviews import GetReviewUseCase, ListReviewsUseCase
from infrastructure.db.repositories.job_repository import PostgresJobRepository
from infrastructure.db.repositories.repo_repository import PostgresRepoRepository
from infrastructure.db.repositories.review_repository import PostgresReviewRepository

router = APIRouter(tags=["reviews"])


@router.get("/reviews", response_model=PaginatedResponse)
async def list_reviews(
    user: CurrentUser,
    session: DbSession,
    repo_id: UUID | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
) -> PaginatedResponse:
    use_case = ListReviewsUseCase(
        PostgresReviewRepository(session),
        PostgresRepoRepository(session),
    )
    return await use_case.execute(user, repo_id=repo_id, page=page, limit=limit)


@router.get("/reviews/{review_id}", response_model=ReviewDetailDTO)
async def get_review(
    review_id: UUID,
    user: CurrentUser,
    session: DbSession,
) -> ReviewDetailDTO:
    use_case = GetReviewUseCase(
        PostgresReviewRepository(session),
        PostgresRepoRepository(session),
    )
    return await use_case.execute(user, review_id)


@router.get("/jobs/{job_id}", response_model=JobStatusDTO)
async def get_job(
    job_id: UUID,
    user: CurrentUser,
    session: DbSession,
) -> JobStatusDTO:
    use_case = GetJobUseCase(
        PostgresJobRepository(session),
        PostgresRepoRepository(session),
    )
    return await use_case.execute(user, job_id)
