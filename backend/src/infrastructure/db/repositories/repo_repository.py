from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.repository import Repository
from domain.repositories.i_repo_repository import IRepoRepository, UpsertRepositoryParams
from infrastructure.db.models.repository import RepositoryORM
from infrastructure.db.repositories.mappers import to_repository_entity


class PostgresRepoRepository(IRepoRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_github_id(self, github_id: int) -> Repository | None:
        result = await self._session.execute(
            select(RepositoryORM).where(RepositoryORM.github_id == github_id)
        )
        orm = result.scalar_one_or_none()
        return to_repository_entity(orm) if orm else None

    async def get_by_id(self, repository_id: UUID) -> Repository | None:
        orm = await self._session.get(RepositoryORM, repository_id)
        return to_repository_entity(orm) if orm else None

    async def upsert(self, params: UpsertRepositoryParams) -> Repository:
        result = await self._session.execute(
            select(RepositoryORM).where(RepositoryORM.github_id == params.github_id)
        )
        orm = result.scalar_one_or_none()

        if orm is None:
            orm = RepositoryORM(
                github_id=params.github_id,
                installation_id=params.installation_id,
                owner=params.owner,
                name=params.name,
                full_name=params.full_name,
                default_branch=params.default_branch,
                language=params.language,
            )
            self._session.add(orm)
        else:
            orm.installation_id = params.installation_id
            orm.owner = params.owner
            orm.name = params.name
            orm.full_name = params.full_name
            orm.default_branch = params.default_branch
            orm.language = params.language

        await self._session.commit()
        await self._session.refresh(orm)
        return to_repository_entity(orm)
