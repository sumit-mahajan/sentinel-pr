from uuid import UUID

from fastapi import APIRouter

from api.middleware.auth_middleware import CurrentUser, DbSession
from api.schemas.dashboard import AgentConfigDTO, RepoDTO, UpdateAgentConfigRequest
from application.use_cases.configure_repo import ConfigureRepoUseCase
from application.use_cases.list_repos import ListReposUseCase
from infrastructure.db.repositories.agent_config_repository import PostgresAgentConfigRepository
from infrastructure.db.repositories.repo_repository import PostgresRepoRepository

router = APIRouter(tags=["repos"])


@router.get("/repos", response_model=list[RepoDTO])
async def list_repos(user: CurrentUser, session: DbSession) -> list[RepoDTO]:
    use_case = ListReposUseCase(
        PostgresRepoRepository(session),
        PostgresAgentConfigRepository(session),
    )
    return await use_case.execute(user)


@router.get("/repos/{repo_id}/config", response_model=AgentConfigDTO)
async def get_repo_config(
    repo_id: UUID,
    user: CurrentUser,
    session: DbSession,
) -> AgentConfigDTO:
    use_case = ConfigureRepoUseCase(
        PostgresRepoRepository(session),
        PostgresAgentConfigRepository(session),
    )
    return await use_case.get_config(user, repo_id)


@router.patch("/repos/{repo_id}/config", response_model=AgentConfigDTO)
async def update_repo_config(
    repo_id: UUID,
    body: UpdateAgentConfigRequest,
    user: CurrentUser,
    session: DbSession,
) -> AgentConfigDTO:
    use_case = ConfigureRepoUseCase(
        PostgresRepoRepository(session),
        PostgresAgentConfigRepository(session),
    )
    return await use_case.update_config(user, repo_id, body)
