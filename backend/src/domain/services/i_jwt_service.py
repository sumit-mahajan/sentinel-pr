from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class JwtPayload:
    sub: UUID
    github_id: int
    login: str


class IJwtService(ABC):
    @abstractmethod
    def create_token(self, *, user_id: UUID, github_id: int, login: str) -> str:
        """Issue a signed session JWT."""

    @abstractmethod
    def decode_token(self, token: str) -> JwtPayload:
        """Validate and decode a session JWT."""
