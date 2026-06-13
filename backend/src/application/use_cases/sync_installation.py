from uuid import UUID

import structlog

from domain.repositories.i_installation_repository import (
    IInstallationRepository,
    UpsertInstallationParams,
)
from domain.repositories.i_repo_repository import IRepoRepository, UpsertRepositoryParams
from domain.services.i_github_app_client import IGithubAppClient

logger = structlog.get_logger()


class SyncInstallationUseCase:
    """Upsert installation and sync accessible repositories from GitHub."""

    def __init__(
        self,
        installation_repo: IInstallationRepository,
        repo_repo: IRepoRepository,
        github_client: IGithubAppClient,
    ) -> None:
        self._installation_repo = installation_repo
        self._repo_repo = repo_repo
        self._github_client = github_client

    async def execute(
        self,
        *,
        installation_id: int,
        account_login: str,
        account_type: str,
        account_avatar_url: str | None,
    ) -> UUID:
        installation = await self._installation_repo.upsert(
            UpsertInstallationParams(
                installation_id=installation_id,
                account_login=account_login,
                account_type=account_type,
                account_avatar_url=account_avatar_url,
            )
        )

        repos = await self._github_client.list_installation_repositories(installation_id)
        for repo_summary in repos:
            await self._repo_repo.upsert(
                UpsertRepositoryParams(
                    github_id=repo_summary.github_id,
                    installation_id=installation.id,
                    owner=repo_summary.owner,
                    name=repo_summary.name,
                    full_name=repo_summary.full_name,
                    default_branch=repo_summary.default_branch,
                    language=repo_summary.language,
                )
            )

        log = logger.bind(
            installation_id=installation_id,
            account_login=account_login,
            repo_count=len(repos),
        )
        await log.ainfo("installation_synced")
        return installation.id
