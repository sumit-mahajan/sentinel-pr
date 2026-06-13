from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from domain.entities.github_installation import GithubInstallation


class UpsertInstallationParams:
    def __init__(
        self,
        *,
        installation_id: int,
        account_login: str,
        account_type: str,
        account_avatar_url: str | None,
    ) -> None:
        self.installation_id = installation_id
        self.account_login = account_login
        self.account_type = account_type
        self.account_avatar_url = account_avatar_url


class IInstallationRepository(ABC):
    @abstractmethod
    async def get_by_installation_id(self, installation_id: int) -> GithubInstallation | None:
        """Find installation by GitHub installation ID."""

    @abstractmethod
    async def get_by_id(self, installation_uuid: UUID) -> GithubInstallation | None:
        """Find installation by internal UUID."""

    @abstractmethod
    async def upsert(self, params: UpsertInstallationParams) -> GithubInstallation:
        """Create or update installation record."""

    @abstractmethod
    async def update_access_token(
        self,
        installation_uuid: UUID,
        *,
        access_token_encrypted: str,
        access_token_expires_at: datetime,
    ) -> GithubInstallation:
        """Cache encrypted installation access token."""
