from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.user import User


@dataclass
class UpsertUserParams:
    github_id: int
    login: str
    email: str | None
    avatar_url: str | None


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_github_id(self, github_id: int) -> User | None:
        """Find user by GitHub numeric ID."""

    @abstractmethod
    async def upsert(self, params: UpsertUserParams) -> User:
        """Create or update a dashboard user."""
