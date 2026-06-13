from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.github_installation import GithubInstallation
from domain.errors import EntityNotFoundError
from domain.repositories.i_installation_repository import (
    IInstallationRepository,
    UpsertInstallationParams,
)
from infrastructure.db.models.installation import GithubInstallationORM
from infrastructure.db.repositories.mappers import to_installation_entity


class PostgresInstallationRepository(IInstallationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_installation_id(self, installation_id: int) -> GithubInstallation | None:
        result = await self._session.execute(
            select(GithubInstallationORM).where(
                GithubInstallationORM.installation_id == installation_id
            )
        )
        orm = result.scalar_one_or_none()
        return to_installation_entity(orm) if orm else None

    async def get_by_id(self, installation_uuid: UUID) -> GithubInstallation | None:
        orm = await self._session.get(GithubInstallationORM, installation_uuid)
        return to_installation_entity(orm) if orm else None

    async def upsert(self, params: UpsertInstallationParams) -> GithubInstallation:
        result = await self._session.execute(
            select(GithubInstallationORM).where(
                GithubInstallationORM.installation_id == params.installation_id
            )
        )
        orm = result.scalar_one_or_none()

        if orm is None:
            orm = GithubInstallationORM(
                installation_id=params.installation_id,
                account_login=params.account_login,
                account_type=params.account_type,
                account_avatar_url=params.account_avatar_url,
            )
            self._session.add(orm)
        else:
            orm.account_login = params.account_login
            orm.account_type = params.account_type
            orm.account_avatar_url = params.account_avatar_url

        await self._session.commit()
        await self._session.refresh(orm)
        return to_installation_entity(orm)

    async def update_access_token(
        self,
        installation_uuid: UUID,
        *,
        access_token_encrypted: str,
        access_token_expires_at: datetime,
    ) -> GithubInstallation:
        orm = await self._session.get(GithubInstallationORM, installation_uuid)
        if orm is None:
            raise EntityNotFoundError(f"Installation {installation_uuid} not found")

        orm.access_token_encrypted = access_token_encrypted
        orm.access_token_expires_at = access_token_expires_at
        await self._session.commit()
        await self._session.refresh(orm)
        return to_installation_entity(orm)
