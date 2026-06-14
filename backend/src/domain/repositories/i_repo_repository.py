from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.repository import Repository


class UpsertRepositoryParams:
    def __init__(
        self,
        *,
        github_id: int,
        installation_id: UUID,
        owner: str,
        name: str,
        full_name: str,
        default_branch: str,
        language: str | None,
    ) -> None:
        self.github_id = github_id
        self.installation_id = installation_id
        self.owner = owner
        self.name = name
        self.full_name = full_name
        self.default_branch = default_branch
        self.language = language


class IRepoRepository(ABC):
    @abstractmethod
    async def get_by_github_id(self, github_id: int) -> Repository | None:
        """Find repository by GitHub numeric ID."""

    @abstractmethod
    async def get_by_id(self, repository_id: UUID) -> Repository | None:
        """Find repository by internal UUID."""

    @abstractmethod
    async def upsert(self, params: UpsertRepositoryParams) -> Repository:
        """Create or update a repository record."""

    @abstractmethod
    async def list_accessible_for_login(self, login: str) -> list[Repository]:
        """Return repos the user can access via installation or ownership."""

    @abstractmethod
    async def update_is_active(self, repository_id: UUID, is_active: bool) -> Repository:
        """Enable or disable review for a repository."""
